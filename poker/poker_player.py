from poker.poker_hand import PokerHand

class PokerPlayer:

    def __init__(self, name, starting_money):
        self.name = name
        self.personal_cards = []
        self.table_cards = []
        self.hand = PokerHand()
        self.money = starting_money
        self.accurateHand = True
        self.currBet = 0

    def __str__(self):
        res = self.name + " (" + str(self.money) + ")\nPERSONAL CARDS:\n"
        for card in self.personal_cards:
            res += str(card) + "\n"
        res += "TABLE CARDS:\n"
        for card in self.table_cards:
            res += str(card) + "\n"
        res += "BEST HAND:\n" + str(self.get_hand()) + "\n\n"
        return res

    def blind(self, amount):
        self.money -= amount

    def call(self, currBet):
        amount = currBet - self.currBet
        self.money -= amount
        return amount

    def raisee(self, currBet):
        amount = int(input("Raise to: "))
        if amount < currBet:
            print("Need to raise more or call")
            self.turn_call(currBet)
        self.money -= amount - self.currBet
        return amount - self.currBet

    def fold():
        return "folded"

    def turn_call(self, currBet):
        decision = str(input("Call (c) | Raise (r) | Fold (f) "))
        if decision == "c":
            return self.call(currBet)
        if decision == "r":
            return self.raisee(currBet)
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

    def turn(self, currBet):
        print("Current Bet: " + str(currBet))
        if self.currBet != currBet:
            return self.turn_call(currBet)
        return self.turn_check()


    def recieve_deal(self, card):
        self.personal_cards.append(card)
        self.hand.add_card(card)
        self.accurateHand = False

    def update_table(self, card):
        self.table_cards.append(card)
        self.hand.add_card(card)
        self.accurateHand = False

    def clear_cards(self):
        self.personal_cards = []
        self.table_cards = []

    def get_hand(self):
        if not self.accurateHand:
            self.hand.update()
            self.accurateHand = True
        return self.hand
