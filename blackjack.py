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
    
    def split(self):
        new_hand = BJHand()
        new_hand.add_card(self.cards[1])
        new_hand.just_split = True
        self.value = 0
        self.add_value(self.cards[0])
        self.cards = [self.cards[0]]
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

    def __init__(self, init_money):
        self.money = init_money
        self.reset()

    def __str__(self):
        hands = [str(hand) for hand in self.hands]
        res = f""
        for hand in hands:
            res += f"{hand}\n\n"
        return res

    def reset(self):
        self.hands = []
        self.num_hands = 0
        self.bets = []

    def set_num_hands(self):
        hands = 0
        while not isinstance(hands, int) or hands < 1 or hands > 3:
            hands = input("How many hands do you wish to play: ")
            if hands.isnumeric():
                hands = int(hands)
        print()
        self.num_hands = hands
        for i in range(self.num_hands):
            self.hands.append(BJHand()) 

    def set_bet(self, min, max):
        bet = 0
        while not isinstance(bet, int) or bet < min or bet > max:
            print(f"money: {self.money}\n\n")
            print(f"max bet: {max}\nmin bet: {min}\n\n")
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
        choice = None
        while choice not in options:
            print(f"dealer:\n{dealer} \n")
            print(f"player:\n{self.hands[index]} \n")
            print(f"options: {options}")
            choice = input()
            print()
        return choice


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

    def __init__(self, decks=1):
        self.min_bet = 25
        self.max_bet = 3000
        self.dealer = Dealer()
        self.player = Player(10000)
        self.deck = Deck(BJCard, decks)
        self.decks = decks

    def handle_player(self, index):
        if self.player.hands[index].just_split:
            self.player.add_card(self.deck.deal(), index)
            self.player.hands[index].just_split = False
        if self.player.hands[index].value == 21:
            return
        decision = self.player.decision(self.dealer, index)
        while not self.player.hands[index].busted and decision == "hit":
            self.player.add_card(self.deck.deal(), index)
            if not self.player.hands[index].busted:
                decision = self.player.decision(self.dealer, index)
            else:
                print("BUSTED\n")
        if decision == "double":
            self.player.add_card(self.deck.deal(), index)
            self.player.bets[index] *= 2
        if decision == "split":
            self.player.hands.insert(index + 1, self.player.hands[index].split())
            self.player.bets.insert(index + 1, self.player.bets[index])
            self.player.num_hands += 1
            return index
        return index + 1

    def handle_dealer(self):
        self.dealer.turn = True
        while self.dealer.hand.value < 17 or (self.dealer.hand.value == 17 and self.dealer.hand.soft):
            self.dealer.add_card(self.deck.deal())

    def handle_winning(self, index):
        print(f"player:\n{self.player.hands[index]}\n")
        if self.player.hands[index] == self.dealer.hand:
            print("push\n")
            return
        if self.player.hands[index] < self.dealer.hand:
            print(f"lost {self.player.bets[index]}\n")
            self.player.money -= self.player.bets[index]
            return
        if len(self.player.hands[index]) == 2 and self.player.hands[index].value == 21:
            self.player.money += self.player.bets[index] * (3 / 2)
            print(f"won {self.player.bets[index] * (3/2)} (Black Jack pays 3 to 2)\n")
            return
        self.player.money += self.player.bets[index]
        print(f"won {self.player.bets[index]}\n")

    def reset(self):
        self.player.reset()
        self.dealer.reset()

    def dealer_bj(self):
        if self.dealer.hand.value == 21:
            print("Dealer BJ\n")
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
        print(f"dealer:\n{self.dealer}\n")
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


def getPlay():
    p = input("Play again? (y/n): ")
    if p == "y":
        return True
    if p == "n":
        return False
    return getPlay()

if __name__ == "__main__":
    game = BlackJack(2)
    play = True
    while play:
        game.round()
        play = getPlay()
