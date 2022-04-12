from random import shuffle

#This is the card object
#A card can have a suite and a value
#value is represented both as a string and a number
#A = 14, K = 13, Q = 12, J = 11
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

    #converts the string value to the numeric value
    def get_poker_val(self):
        if self.value == "J":
            return 11
        if self.value == "Q":
            return 12
        if self.value == "K":
            return 13
        if self.value == "A":
            return 14
        return int(self.value)
    
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
        return self.bj_val == other.bj_val

#This is the deck object
class Deck:
    #No values are passed to it
    #when created it will contain a list of 52 unique cards in random order
    #num_decks default is 1 but if another value is given
    def __init__(self, type, num_decks=1):
        self.type = type
        if num_decks < 1:
            num_decks = 1
        self.num_decks = num_decks // 1
        self.deck = None
        self.shuffle()

    #returns lenght of deck
    def __len__(self):
        return len(self.deck)

    #likely does not need to be used other than error checking
    #string representation of deck was just to make sure shuffle worked
    def __str__(self):
        deckString = ""
        for card in self.deck:
            deckString += str(card) + "\n"
        return deckString

    #this is the main function of deck
    #sets self.deck to a list of card objects that simulates a shuffled deck
    def shuffle(self):
        suites = ["Spades", "Clubs", "Diamonds", "Hearts"]
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        cards = [self.type(suite, value) 
                 for suite in suites 
                 for value in values] * self.num_decks
        shuffle(cards)
        self.deck = cards

    #returns the card on top and removes it from the deck
    def deal(self):
        card = self.deck[0]
        self.deck = self.deck[1:]
        return card
    
    #the card on top is removed from the deck without being returned
    def burn(self):
        self.deck = self.deck[1:]