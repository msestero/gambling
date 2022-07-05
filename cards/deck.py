from random import shuffle

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

    def pluck(self, num_value, suite=None):
        for pos, card in enumerate(self.deck):
            if card.num_val == num_value and (suite is None or suite == card.suite):
                res = card
                print(res, pos)
                self.deck = self.deck[:pos] + self.deck[pos+1:]
                return res
                

    #returns the card on top and removes it from the deck
    def deal(self):
        card = self.deck[0]
        self.deck = self.deck[1:]
        return card
    
    #the card on top is removed from the deck without being returned
    def burn(self):
        self.deck = self.deck[1:]