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
        
    def add_card(self, card):
        self.cards.append(card)
        self.add_value(card)
        self.check_busted()

    def __str__(self):
        res = f""
        for card in self.cards:
            res += f"{str(card)}\n"
        res += f"{self.value}"
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
        self.hand = BJHand()
        self.bet = 0

    def __str__(self):
        return str(self.hand)

    def reset(self):
        self.hand.reset()

    def set_bet(self, min, max):
        bet = 0
        while not isinstance(bet, int) or bet < min or bet > max:
            print(f"money: {self.money}\n\n")
            print(f"max bet: {max}\nmin bet: {min}\n\n")
            bet = input("bet amount: ")
            if bet.isnumeric():
                bet = int(bet)
        print()
        self.bet = bet

    def add_card(self, card):
        self.hand.add_card(card)

    def decision(self, dealer):
        options = ["hit", "stand"]
        if self.hand.can_double:
            options.append("double")
        choice = None
        while choice not in options:
            print(f"dealer:\n{dealer} \n")
            print(f"player:\n{self.hand} \n")
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

    def handle_player(self):
        if self.player.hand.value == 21:
            return
        decision = self.player.decision(self.dealer)
        while not self.player.hand.busted and decision == "hit":
            self.player.add_card(self.deck.deal())
            if not self.player.hand.busted:
                decision = self.player.decision(self.dealer)
            else:
                print("BUSTED\n")
        if decision == "double":
            self.player.add_card(self.deck.deal())
            self.player.bet *= 2

    def handle_dealer(self):
        self.dealer.turn = True
        while self.dealer.hand.value < 17 or (self.dealer.hand.value == 17 and self.dealer.hand.soft):
            self.dealer.add_card(self.deck.deal())

    def handle_winning(self):
        print(f"dealer:\n{self.dealer}\n")
        print(f"player:\n{self.player}\n")
        if self.player.hand == self.dealer.hand:
            print("push")
            return
        if self.player.hand < self.dealer.hand:
            print("loser")
            self.player.money -= self.player.bet
            return
        if len(self.player.hand) == 2 and self.player.hand.value == 21:
            self.player.money += self.player.bet * (3 / 2)
            print("winner (Black Jack pays 3 to 2)")
            return
        self.player.money += self.player.bet
        print("winner")

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
        self.player.set_bet(self.min_bet, self.max_bet)
        self.deal()
        if not self.dealer_bj():
            self.handle_player()
            self.handle_dealer()
        self.handle_winning()
        self.reset()

    def deal(self):
        if len(self.deck) / (52 * self.decks) <= 0.5:
            self.deck.shuffle()
        for i in range(2):
            self.player.add_card(self.deck.deal())
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
