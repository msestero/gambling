from poker.poker_hand import PokerHand
import os

class PokerPlayer:

    def __init__(self, name, starting_money):
        self.name = name
        self.personal_cards = []
        self.table_cards = []
        self.hand = PokerHand()
        self.money = starting_money
        self.accurate_hand = True
        self.in_game = False
        self.had_chance_bet = False
        self.curr_bet = 0
    
    def __lt__(self, other):
        if not self.in_game:
            return True
        return self.hand < other.hand

    def __eq__(self, other):
        return self.hand == other.hand

    def __str__(self):
        res = self.name + " (" + str(self.money) + ")\nPERSONAL CARDS:\n"
        for card in self.personal_cards:
            res += str(card) + "\n"
        res += "TABLE CARDS:\n"
        for card in self.table_cards:
            res += str(card) + "\n"
        res += "BEST HAND:\n" + str(self.get_hand()) + "\n\n"
        return res

    def end_bet_round(self):
        self.had_chance_bet = False
        self.curr_bet = 0

    def blind(self, amount):
        self.money -= amount
        self.curr_bet = amount

    def call(self, curr_bet):
        amount = curr_bet - self.curr_bet
        self.money -= amount
        self.curr_bet = curr_bet
        return amount

    def raisee(self, curr_bet):
        amount = int(input("Raise to: "))
        if amount <= curr_bet:
            print("Need to raise more or call")
            self.turn_call(curr_bet)
        self.money -= amount - self.curr_bet
        self.curr_bet = amount
        return amount - self.curr_bet

    def fold(self):
        self.in_game = False
        return "folded"

    def turn_call(self, curr_bet):
        decision = str(input("Call (c) | Raise (r) | Fold (f) "))
        if decision == "c":
            return self.call(curr_bet)
        if decision == "r":
            return self.raisee(curr_bet)
        if decision == "f":
            return self.fold()

    def turn_check(self):
        decision = str(input("Check (c) | Raise (r) | Fold (f) "))
        if decision == "c":
            return 0
        if decision == "r":
            return self.raisee(0)
        if decision == "f":
            return self.fold()

    def turn(self, curr_bet):
        os.system('clear')
        print("Current Table Bet: " + str(curr_bet))
        print("Current Personal Bet: " + str(self.curr_bet) + "\n")
        print(self)
        self.had_chance_bet = True
        if self.curr_bet != curr_bet:
            return self.turn_call(curr_bet)
        return self.turn_check()


    def recieve_deal(self, card):
        self.personal_cards.append(card)
        self.hand.add_card(card)
        self.accurate_hand = False

    def add_card_table(self, card):
        self.table_cards.append(card)
        self.hand.add_card(card)
        self.accurate_hand = False

    def clear_cards(self):
        self.personal_cards = []
        self.table_cards = []

    def get_hand(self):
        if not self.accurate_hand:
            self.hand.update()
            self.accurate_hand = True
        return self.hand
