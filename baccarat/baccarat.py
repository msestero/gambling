from cards.deck import Deck
from cards.deck import BJCard

import os

class BaccaratHand:

    def __init__(self):
        self.cards = []
        self.value = 0

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.num_val
        if self.value >= 10:
            self.value -= 10

class BaccaratPlayer:
    
    def __init__(self):
        self.banker_bet = 0
        self.dragon_bet = 0
        self.total_bet = 0
        self.money = 0

    def set_bet(self, true_count):
        self.banker_bet = 10
        self.dragon_bet = 0
        # if true_count >= 4:
        #     self.dragon_bet = 10
        self.total_bet = self.banker_bet + self.dragon_bet


class Baccarat:

    def __init__(self):
        self.banker = BaccaratHand()
        self.player = BaccaratHand()
        self.player_bet = BaccaratPlayer()
        self.deck = Deck(BJCard, num_decks=6)
        self.running_count = 0
        self.true_count = 0

    def deal_card(self):
        card = self.deck.deal()
        if card.num_val in [4, 5, 6, 7]:
            self.running_count -= 1
        if card.num_val in [8, 9]:
            self.running_count += 2
        self.true_count = 52 * self.running_count / len(self.deck)
        return card

    def deal(self):
        if len(self.deck) < 26:
            self.deck.shuffle()
            self.deck.shuffle()
        for i in range(2):
            self.player.add_card(self.deal_card())
            self.banker.add_card(self.deal_card())
    
    def additional_deal(self):
        if self.banker.value >= 8 or self.player.value >= 8:
            return
        if self.player.value > 5:
            if self.banker.value <= 5:
                self.banker.add_card(self.deal_card())
            return
        player_card = self.deal_card()
        self.player.add_card(player_card)
        val = player_card.num_val
        if val >= 10:
            val -= 10
        chart = [[True , True , True , True , True , True , True , True , True , True],
                 [True , True , True , True , True , True , True , True , True , True],
                 [True , True , True , True , True , True , True , True , True , True],
                 [True , True , True , True , True , True , True , True , False, True],
                 [False, False, True , True , True , True , True , True , False, False],
                 [False, False, False, False, True , True , True , True , False, False],
                 [False, False, False, False, False, False, True , True , False, False],
                 [False, False, False, False, False, False, False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False],
                 [False, False, False, False, False, False, False, False, False, False]]
        if chart[self.banker.value][val]:
            self.banker.add_card(self.deal_card())

    def winner(self):
        if self.player > self.banker:
            self.player_bet.money -= self.player_bet.total_bet
            return self.player_bet.money
        if self.player == self.banker:
            self.player_bet.money -= self.player_bet.dragon_bet
            return self.player_bet.money
        if self.banker.value == 7 and len(self.banker.cards) == 3:
            self.player_bet.money += self.player_bet.dragon_bet * 40 #+ self.player_bet.banker_bet
            return self.player_bet.money
        self.player_bet.money += self.player_bet.banker_bet
        self.player_bet.money -= self.player_bet.dragon_bet
        return self.player_bet.money

    def round(self):
        self.player_bet.set_bet(self.true_count)
        self.banker = BaccaratHand()
        self.player = BaccaratHand()
        self.deal()
        self.additional_deal()
        return self.winner()

    def play(self, rounds):
        results = []
        for i in range(rounds):
            results.append(self.round())
            divisor = rounds // 10
            percent = (i * 100) // rounds
            if i % (divisor / 10) == 0:
                os.system('clear')
                print(f"{percent}%\n\n")
        return results
