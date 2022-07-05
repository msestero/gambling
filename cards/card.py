#This is the card object
#A card can have a suite and a value
#value is represented both as a string
class Card:
    #suite is either Spades, Clubs, Hearts, Diamonds
    #value is one of ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    def __init__(self, suite, value):
        self.check_valid(suite, value)
        self.suite = suite
        self.value = value

    def check_valid(self, suite, value):
        if suite not in ["Spades", "Hearts", "Clubs", "Diamonds"]:
            raise ValueError("suite must be either Spades, Hearts, Clubs, or Diamonds")
        if value not in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            raise ValueError("Incorrect value passed to card")

    #string representation to display card to terminal
    def __str__(self):
        return self.value + " of " + self.suite

    
class PokerCard(Card):

    def __init__(self, suite, value):
        super(PokerCard, self).__init__(suite, value)
        self.num_val = self.get_num_val()

    #less than function to compare cards
    #suites have no affect on value
    def __lt__(self, other):
        return self.num_val < other.num_val

    def get_num_val(self):
        if self.value == "J":
            return 11
        if self.value == "Q":
            return 12
        if self.value == "K":
            return 13
        if self.value == "A":
            return 14
        return int(self.value)

    def __eq__(self, other):
        return self.num_val == other.num_val

class BJCard(Card):

    def __init__(self, suite, value):
        super(BJCard, self).__init__(suite, value)
        self.num_val = self.get_num_val()

    def get_num_val(self):
        if self.value == "J":
            return 10
        if self.value == "Q":
            return 10
        if self.value == "K":
            return 10
        if self.value == "A":
            return 11
        return int(self.value)
    
    #equal to function to compare cards
    #useful for splitting in BJ
    def __eq__(self, other):
        return self.num_val == other.num_val