from cards.deck import Deck, PokerCard
from poker.poker_hand import PokerHand
from poker.poker_player import PokerPlayer      
class PokerGame:

    def __init__(self, buyin, max_num_buyin, little_blind):
        self.buyin = buyin
        self.max_buyin = buyin * max_num_buyin
        self.little_blind = little_blind
        self.pot = 0
        self.table_cards = []
        self.players = [None] * 9
        self.seats_taken = []
        self.dealer_pos = 1
        self.deck = Deck(PokerCard)
        self.curr_bet = 0

    def addPlayer(self, player, pos):
        if self.players[pos]:
            print("Position Already taken")
            return
        self.players[pos] = player
        self.seats_taken.append(pos)

    def deal(self):
        for seat in self.seats_taken:
            self.players[seat].recieve_deal(self.deck.deal())
        for seat in self.seats_taken:
            self.players[seat].recieve_deal(self.deck.deal())

    def blinds(self):
        littleBlind = None
        bigBlind = None
        pos = self.dealer_pos + 1
        while bigBlind is None:
            player = self.players[pos % 9]
            if player and not littleBlind:
                littleBlind = player
            elif player and littleBlind:
                bigBlind = player
            pos += 1
        littleBlind.blind(self.little_blind)
        bigBlind.blind(self.little_blind * 2)
        self.pot = 3 * self.little_blind
        self.curr_bet = 2 * self.little_blind

    # def betting(self):
    #     initial_better = self.dealer_pos

    def order_seats_taken(self):
        self.seats_taken.sort()
        dealer_index = self.seats_taken.index(self.dealer_pos)
        self.seats_taken = self.seats_taken[dealer_index:] + self.seats_taken[:dealer_index]
        self.seats_taken = self.seats_taken[1:] + [self.seats_taken[0]]


    def play_round(self):
        if len(self.seats_taken) < 2:
            raise("not enough players")
        self.order_seats_taken()
        self.deal()
        self.blinds()
        for player in self.players:
            print(player)

if __name__ == "__main__":
    game = PokerGame(100, 5, 5)
    player1 = PokerPlayer("player1", 100)
    player2 = PokerPlayer("player2", 100)
    game.addPlayer(player1, 0)
    game.addPlayer(player2, 1)
    game.play_round()
