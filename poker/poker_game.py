from cards.deck import Deck
from cards.card import PokerCard
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
        self.num_players = 0
        self.dealer_pos = 0
        self.deck = Deck(PokerCard)
        self.curr_bet = 0

    # def addPlayer(self):
    #     name = input("NAME: ")
    #     cash = input("CASH: ")
    #     if cash.isnumeric():
    #         self.autoAddPlayer(name, int(cash))
    #         return
    #     print("invalid input")
    #    self.addPlayer()

    def addPlayer(self, player, pos):
        if self.players[pos]:
            print("Position Already taken")
            return
        self.players[pos] = player
        self.seats_taken.append(pos)
        self.num_players += 1

    def deal(self):
        for seat in self.seats_taken:
            self.players[seat].recieve_deal(self.deck.deal())
        for seat in self.seats_taken:
            self.players[seat].recieve_deal(self.deck.deal())

    def blinds(self):
        littleBlind = None
        bigBlind = None
        pos = 0
        while bigBlind is None:
            player = self.players[self.seats_taken[pos % self.num_players]]
            if player and not littleBlind:
                littleBlind = player
            elif player and littleBlind:
                bigBlind = player
            pos += 1
        littleBlind.blind(self.little_blind)
        bigBlind.blind(self.little_blind * 2)
        self.curr_bet = 2 * self.little_blind
        for seat in self.seats_taken:
            self.players[seat].in_game = True

    # def betting(self):
    #     initial_better = self.dealer_pos

    def order_seats_taken(self):
        self.seats_taken.sort()
        self.seats_taken = self.seats_taken[self.dealer_pos:] + self.seats_taken[:self.dealer_pos]
        self.seats_taken = self.seats_taken[1:] + [self.seats_taken[0]]

    def keep_going(self):
        res = 0
        for seat in self.seats_taken:
            if self.players[seat].in_game:
                res += 1
        return res > 1

    def bets_good(self):
        for seat in self.seats_taken:
            player = self.players[seat]
            if player.in_game and (player.curr_bet != self.curr_bet or not player.had_chance_bet) and self.keep_going():
                return False
        return True

    def bets(self, start_pos):
        pos = start_pos
        while not self.bets_good():
            while not self.players[self.seats_taken[pos % self.num_players]].in_game:
                pos += 1
            player = self.players[self.seats_taken[pos % self.num_players]]
            player.turn(self.curr_bet)
            if player.curr_bet > self.curr_bet:
                self.curr_bet = player.curr_bet
            pos += 1
        for seat in self.seats_taken:
            self.pot += self.players[seat].curr_bet
            self.players[seat].end_bet_round()
            self.curr_bet = 0
        print("bets good")

    def add_card_players(self, card):
        for seat in self.seats_taken:
            self.players[seat].add_card_table(card)

    def flop(self):
        self.deck.burn()
        for i in range(3):
            card = self.deck.deal()
            self.table_cards.append(card)
            self.add_card_players(card)
        print("done flop")

    def turn(self):
        self.deck.burn()
        card = self.deck.deal()
        self.table_cards.append(card)
        self.add_card_players(card)
        print("done turn")

    def river(self):
        self.deck.burn()
        card = self.deck.deal()
        self.table_cards.append(card)
        self.add_card_players(card)
        print("done river")

    def get_winner(self):
        not_none = list(filter(lambda x : x is not None, self.players))
        ranks = sorted(not_none, reverse=True)
        winners = []
        winners.append(ranks[0])
        for player in ranks[1:]:
            if player == winners[0] and player.in_game:
                winners.append(player)
        print("WINNER(S):", list(map(lambda x : x.name, winners)))
        winnings = self.pot // len(winners)
        for winner in winners:
            winner.money += winnings
        

    def play_round(self):
        if len(self.seats_taken) < 2:
            raise("not enough players")
        self.order_seats_taken()
        self.deal()
        self.blinds()
        self.bets(2)
        self.flop()
        self.bets(0)
        self.turn()
        self.bets(0)
        self.river()
        self.bets(0)
        self.get_winner()


if __name__ == "__main__":
    game = PokerGame(100, 5, 5)
    player1 = PokerPlayer("player1", 100)
    player2 = PokerPlayer("player2", 100)
    player3 = PokerPlayer("player3", 100)
    player4 = PokerPlayer("player4", 100)
    game.addPlayer(player1, 1)
    game.addPlayer(player2, 2)
    game.addPlayer(player3, 3)
    game.addPlayer(player4, 4)
    game.play_round()
    for player in game.players:
        print(player)
