from deck import Deck
from deck import BJCard

class BJHand:

    def __init__(self):
        self.reset()

    def reset(self):
        self.cards = []
        self.value = 0

        self.busted = False
        self.soft = False

        self.can_double = True

        self.can_surrender = True
        self.surrendered = False

        self.can_split = False
        self.just_split = False

        self.num_ace = 0
        self.ace_1_val = 0

    def __len__(self):
        return len(self.cards)

    def check_busted(self):
        if self.value > 21:
            self.busted = True

    def reduce(self):
        if self.num_ace > self.ace_1_val:
            self.value -= 10
            self.ace_1_val += 1
        if self.num_ace == self.ace_1_val:
            self.soft = False

    def add_value(self, card):
        if card.num_val == 11:
            self.soft = True
            self.num_ace += 1
        self.value += card.num_val
        if self.value > 21:
            self.reduce()
        if len(self.cards) > 2:
            self.can_double = False
            self.can_split = False
        if len(self.cards) == 2 and self.cards[0] == self.cards[1]:
            self.can_split = True
        else:
            self.can_split = False
    
    def split(self):
        new_hand = BJHand()
        new_hand.add_card(self.cards[1])
        new_hand.just_split = True
        other_card = self.cards[0]
        self.reset()
        self.add_card(other_card)
        self.just_split = True
        return new_hand
        
    def add_card(self, card):
        self.cards.append(card)
        self.add_value(card)
        self.check_busted()

    def __str__(self):
        res = f""
        for card in self.cards:
            res += f"{str(card)}\n"
        res += f"total: {self.value}"
        return res

    def __lt__(self, other):
        if not isinstance(other, BJHand):
            raise ValueError
        if self.busted:
            return True
        if other.busted:
            return False
        return self.value < other.value

    def __eq__(self, other):
        if not isinstance(other, BJHand):
            raise ValueError
        if self.busted:
            return False
        return self.value == other.value


class Player:

    def __init__(self):
        self.money = self.getMoney()
        self.reset()
        self.hands_played = 0

    def __str__(self):
        hands = [str(hand) for hand in self.hands]
        res = f""
        for hand in hands:
            res += f"{hand}\n\n"
        return res

    def getMoney(self):
        initial_money = None
        while True:
            initial_money = input("Initial Money: ")
            if initial_money.isnumeric():
                return int(initial_money)
            print("\nplease give integer\n")

    def reset(self):
        self.hands = []
        self.num_hands = 0
        self.bets = []

    def set_num_hands(self):
        hands = 0
        while not isinstance(hands, int) or hands < 1 or hands > 3:
            hands = input("\nnum hands: ")
            if hands.isnumeric():
                hands = int(hands)
        print()
        self.num_hands = hands
        for i in range(self.num_hands):
            self.hands.append(BJHand())
        self.hands_played += hands

    def set_bet(self, min, max):
        bet = 0
        while not isinstance(bet, int) or bet < min or bet > max:
            print(f"your money: {self.money}\n")
            print(f"max bet: {max}")
            print(f"min bet: {min}\n")
            bet = input("bet amount: ")
            if bet.isnumeric():
                bet = int(bet)
        print()
        self.bets = [bet] * self.num_hands

    def add_card(self, card, index):
        self.hands[index].add_card(card)

    def decision(self, dealer, index):
        options = ["hit", "stand"]
        if self.hands[index].can_double:
            options.append("double")
        if self.hands[index].can_split:
            options.append("split")
        if self.hands[index].can_surrender:
            options.append("surrender")
        choice = None
        while choice not in options:
            print(f"dealer:\n{dealer} \n")
            print(f"player:\n{self.hands[index]} \n")
            print(f"options: {options}")
            choice = input()
            print()
        self.hands[index].can_surrender = False
        return choice

    def getPlay(self):
        p = input("Play again? (y/n): ")
        if p == "y":
            return True
        if p == "n":
            return False
        return self.getPlay()

class BasicStrategyPlayer(Player):

    def __init__(self, initial_money):
        self.money = initial_money
        self.reset()
        self.hands_played = 0
        self.high = self.money

    def set_num_hands(self):
        self.num_hands = 1
        self.hands = [BJHand()]
        self.hands_played += 1

    def set_bet(self, min, max):
        self.bets = [25]
    
    def decision(self, dealer, index):
        if self.money > self.high:
            self.high = self.money
        if self.hands[index].can_split:
            if self.handle_split(dealer, index):
                self.hands_played += 1
                return "split"
        if self.hands[index].soft:
            return self.handle_soft(dealer, index)
        return self.handle_hard(dealer, index)

    def handle_hard(self, dealer, index):

        player_val = self.hands[index].value
        dealer_card = str(dealer.hand.cards[1].num_val)

        if self.hands[index].can_surrender:
            if player_val == 16 and dealer_card in ["11", "10", "9"]:
                return "surrender"
            if player_val == 15 and dealer_card == "10":
                return "surrender"

        if player_val > 16:
            return "stand"
        if player_val < 9:
            return "hit"

        player_val = str(player_val)

        grid = [["S", "S", "S", "S", "S", "H", "H", "H", "H", "H"],
                ["S", "S", "S", "S", "S", "H", "H", "H", "H", "H"],
                ["S", "S", "S", "S", "S", "H", "H", "H", "H", "H"],
                ["S", "S", "S", "S", "S", "H", "H", "H", "H", "H"],
                ["H", "H", "S", "S", "S", "H", "H", "H", "H", "H"],
                ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],
                ["H", "D", "D", "D", "D", "D", "D", "D", "H", "H"],
                ["H", "D", "D", "D", "D", "H", "H", "H", "H", "H"]]

        rows = {"16" : 0,
                "15" : 1,
                "14" : 2,
                "13" : 3,
                "12" : 4,
                "11" : 5,
                "10" : 6,
                "9"  : 7}
        
        columns = {"2"  : 0,
                   "3"  : 1,
                   "4"  : 2,
                   "5"  : 3,
                   "6"  : 4,
                   "7"  : 5,
                   "8"  : 6,
                   "9"  : 7,
                   "10" : 8,
                   "11" : 9}

        res = grid[rows[player_val]][columns[dealer_card]]

        if res == "S":
            return "stand"
        if res == "H":
            return "hit"
        if self.hands[index].can_double:
            return "double"
        return "hit"

    def handle_soft(self, dealer, index):

        player_val = str(self.hands[index].value)
        dealer_card = str(dealer.hand.cards[1].num_val)

        grid = [["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],
                ["S", "S", "S", "S", "Ds", "S", "S", "S", "S", "S"],
                ["Ds", "Ds", "Ds", "Ds", "Ds", "S", "S", "H", "H", "H"],
                ["H", "D", "D", "D", "D", "H", "H", "H", "H", "H"],
                ["H", "H", "D", "D", "D", "H", "H", "H", "H", "H"],
                ["H", "H", "D", "D", "D", "H", "H", "H", "H", "H"],
                ["H", "H", "H", "D", "D", "H", "H", "H", "H", "H"],
                ["H", "H", "H", "D", "D", "H", "H", "H", "H", "H"]]

        rows = {"20" : 0,
                "19" : 1,
                "18"  : 2,
                "17"  : 3,
                "16"  : 4,
                "15"  : 5,
                "14"  : 6,
                "13"  : 7}
        
        columns = {"2"  : 0,
                   "3"  : 1,
                   "4"  : 2,
                   "5"  : 3,
                   "6"  : 4,
                   "7"  : 5,
                   "8"  : 6,
                   "9"  : 7,
                   "10" : 8,
                   "11" : 9}

        res = grid[rows[player_val]][columns[dealer_card]]

        if res == "S":
            return "stand"
        if res == "H":
            return "hit"
        if self.hands[index].can_double:
            return "double"
        if res == "Ds":
            return "stand"
        return "hit"
        
    def handle_split(self, dealer, index):

        player_pair = str(self.hands[index].cards[0].num_val) + "s"
        dealer_card = str(dealer.hand.cards[1].num_val)

        grid = [[True , True , True , True , True , True , True , True , True , True ],
                [False, False, False, False, False, False, False, False, False, False],
                [True , True , True , True , True , False, True , True , False, False],
                [True , True , True , True , True , True , True , True , True , True ],
                [True , True , True , True , True , True , False, False, False, False],
                [True , True , True , True , True , False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False],
                [False, False, False, True , True , False, False, False, False, False],
                [True , True , True , True , True , True , False, False, False, False],
                [True , True , True , True , True , True , False, False, False, False]]

        rows = {"11s" : 0,
                "10s" : 1,
                "9s"  : 2,
                "8s"  : 3,
                "7s"  : 4,
                "6s"  : 5,
                "5s"  : 6,
                "4s"  : 7,
                "3s"  : 8,
                "2s"  : 9}

        columns = {"2"  : 0,
                   "3"  : 1,
                   "4"  : 2,
                   "5"  : 3,
                   "6"  : 4,
                   "7"  : 5,
                   "8"  : 6,
                   "9"  : 7,
                   "10" : 8,
                   "11" : 9}
        
        return grid[rows[player_pair]][columns[dealer_card]]


    def getPlay(self):
        if self.money >= 25:
            return True
        return False


class Dealer:

    def __init__(self):
        self.hand = BJHand()
        self.turn = False

    def reset(self):
        self.hand.reset()
        self.turn = False

    def add_card(self, card):
        self.hand.add_card(card)
    
    def __str__(self):
        if not self.turn:
            return str(self.hand.cards[1])
        return str(self.hand)


class BlackJack:

    def __init__(self, player, decks=1, show_terminal=True):
        self.min_bet = 25
        self.max_bet = 3000
        self.dealer = Dealer()
        self.player = player
        self.deck = Deck(BJCard, decks)
        self.decks = decks
        self.show_terminal = show_terminal

    def terminal(self, value):
        if self.show_terminal:
            print(value)

    def handle_player(self, index):
        if self.player.hands[index].just_split:
            self.player.add_card(self.deck.deal(), index)
            self.player.hands[index].just_split = False
        if self.player.hands[index].value == 21:
            return index + 1
        decision = self.player.decision(self.dealer, index)
        while self.player.hands[index].value < 21 and decision == "hit":
            self.player.add_card(self.deck.deal(), index)
            if self.player.hands[index].value < 21:
                decision = self.player.decision(self.dealer, index)
            else:
                self.terminal("BUSTED\n")
        if decision == "double":
            self.player.add_card(self.deck.deal(), index)
            self.player.bets[index] *= 2
        if decision == "split":
            self.player.hands.insert(index + 1, self.player.hands[index].split())
            self.player.bets.insert(index + 1, self.player.bets[index])
            self.player.num_hands += 1
            return index
        if decision == "surrender":
            self.player.bets[index] /= 2
            self.player.hands[index].surrendered = True
        return index + 1

    def handle_dealer(self):
        self.dealer.turn = True
        while self.dealer.hand.value < 17 or (self.dealer.hand.value == 17 and self.dealer.hand.soft):
            self.dealer.add_card(self.deck.deal())

    def handle_winning(self, index):
        self.terminal(f"player:\n{self.player.hands[index]}\n")
        if len(self.player.hands[index]) == 2 and self.player.hands[index].value == 21 and len(self.dealer.hand) > 2:
            self.player.money += self.player.bets[index] * (3 / 2)
            self.terminal(f"won {self.player.bets[index] * (3/2)} (Black Jack pays 3 to 2)\n")
            return
        if self.player.hands[index].surrendered:
            self.terminal(f"lost {self.player.bets[index]}\n")
            self.player.money -= self.player.bets[index]
            return
        if self.player.hands[index] == self.dealer.hand:
            self.terminal("push\n")
            return
        if self.player.hands[index] < self.dealer.hand:
            self.terminal(f"lost {self.player.bets[index]}\n")
            self.player.money -= self.player.bets[index]
            return
        self.player.money += self.player.bets[index]
        self.terminal(f"won {self.player.bets[index]}\n")

    def reset(self):
        self.player.reset()
        self.dealer.reset()

    def dealer_bj(self):
        if self.dealer.hand.value == 21:
            self.terminal("Dealer BJ\n")
            self.dealer.turn = True
            return True
        return False

    def round(self):
        self.player.set_num_hands()
        self.player.set_bet(self.min_bet, self.max_bet)
        self.deal()
        if not self.dealer_bj():
            index = 0
            while index < self.player.num_hands:
                index = self.handle_player(index)
            self.handle_dealer()
        self.terminal(f"dealer:\n{self.dealer}\n")
        for i in range(self.player.num_hands):
            self.handle_winning(i)
        self.reset()

    def deal(self):
        if len(self.deck) / (52 * self.decks) <= 0.5:
            self.deck.shuffle()
        for i in range(2):
            for i in range(self.player.num_hands):
                self.player.add_card(self.deck.deal(), i)
            self.dealer.add_card(self.deck.deal())

    def play(self):
        play = self.player.getPlay()
        count = 0
        while play:
            count += 1
            self.round()
            play = self.player.getPlay()
        self.terminal(f"\n{self.player.money}")
        return self.player.high
