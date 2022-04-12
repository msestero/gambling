from deck import Deck
from deck import BJCard

class BJHand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.busted = False

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.num_val

    def __str__(self):
        res = f""
        for card in self.cards:
            res += f"{str(card)}\n"
        res += f"{self.value}"
        return res

    def __lt__(self, other):
        if not isinstance(other, BJHand):
            raise ValueError
        self.value < other.value


class Player:

    def __init__(self, init_money):
        self.money = init_money
        self.hand = BJHand()
        self.bet = 0

    def set_bet(self, min, max):
        bet = 0
        while not isinstance(bet, int) or bet < min or bet > max:
            print(f"max bet: {max}\nmin bet: {min}\n\n")
            bet = input("bet amount: ")
            if bet.isnumeric():
                bet = int(bet)
        self.bet = bet

    def add_card(self, card):
        self.hand.add_card(card)

    def decision(self, dealer):
        options = ["hit", "stand"]
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

    def add_card(self, card):
        self.hand.add_card(card)
    
    def __str__(self):
        if not self.turn:
            return str(self.BJHand.cards[1])
        return 


class BlackJack:

    def __init__(self, decks=1):
        self.min_bet = 25
        self.max_bet = 3000
        self.dealer = BJHand()
        self.player = Player(10000)
        self.deck = Deck(BJCard, decks)

    def handle_player(self):
        decision = self.player.decision(self.dealer)
        while decision == "hit":
            self.player.add_card(self.deck.deal())
            decision = self.player.decision(self.dealer)

    def round(self):
        self.player.set_bet(self.min_bet, self.max_bet)
        self.deal()
        self.handle_player()   

    def deal(self):
        for i in range(2):
            self.player.add_card(self.deck.deal())
            self.dealer.add_card(self.deck.deal())


if __name__ == "__main__":
    game = BlackJack(2)
    game.round()



