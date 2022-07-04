#This is the hand object
#Each player will have a hand
class PokerHand:

    #No values are give when instantiated because the player does not have any cards
    def __init__(self):
        self.cards = []
        self.hand_name = None
        self.hand_val = 0
        self.best_cards = []

    #returns a string representation of the best formed hand with the given cards
    def __str__(self):
        if self.hand_name is None:
            return "\nNo Cards\n"
        hand_string = self.hand_name
        hand_string += ":\n"
        for card in self.best_cards:
            hand_string += str(card) + "\n"
        return hand_string

    def __eq__(self, other):
        if len(self.best_cards) != len(other.best_cards):
            return False
        for card1, card2 in zip(self.best_cards, other.best_cards):
            if card1 != card2:
                return False
        return True

    def __le__(self, other):
        return ((self == other) or (self < other))

    def __ge__(self, other):
        return ((self > other) or (self == other))

    #Used to compare different hands
    #This is when the round is over and a winner needs to be decided
    def __lt__(self, other):
        self.update()
        if self.hand_val != other.hand_val:
            return self.hand_val < other.hand_val
        shortest_length = min(len(self.best_cards), len(other.best_cards))
        for i in range(shortest_length):
            if self.best_cards[i] < other.best_cards[i]:
                return True
        return False

    # restarts the hand so that a new one does not have to be created
    def clear(self):
        self.cards = []
        self.hand_val = 0
        self.hand_name = None
        self.best_cards = None

    #adds a card to cards and sorts it
    #no other values are changed
    #in order to update the other values self.update() needs to called
    #this is to prevent unnecessary work
    def add_card(self, card):
        self.cards.append(card)
        self.cards.sort(reverse=True)

    #adds multiple cards to cards
    def add_cards(self, cards):
        for card in cards:
            self.add_card(card)

    #given cards matched, return cards in self.cards that are not in matched
    #useful for more complicated hand types
    def getothers(self, matched):
        cards = self.cards[:]
        for card in matched:
            cards.remove(card)
        return cards

    #call update to set:
    #         -hand_val
    #         -hand_name
    #         -best_cards
    #call this to interpret your cards
    def update(self):
        royal = self.royal()
        straightflush = self.straightflush()
        fourofkind = self.fourofkind()
        fullhouse = self.fullhouse()
        flush = self.flush()
        straight = self.straight()
        threeofkind = self.threeofkind()
        twopair = self.twopair()
        pair = self.pair()

        if royal:
            self.hand_name = "royal flush"
            self.best_cards = royal
            self.hand_val = 9
            return

        if straightflush:
            self.hand_name = "straight flush"
            self.best_cards = straightflush
            self.hand_val = 8
            return
        
        if fourofkind:
            self.hand_name = "four of a kind"
            others = self.getothers(fourofkind)
            if len(others) != 0:
                self.best_cards = fourofkind + [others[0]]
            else:
                self.best_cards = fourofkind
            self.hand_val = 7
            return

        if fullhouse:
            self.hand_name = "full house"
            self.best_cards = fullhouse
            self.hand_val = 6
            return

        if flush:
            self.hand_name = "flush"
            self.best_cards = flush
            self.hand_val = 5
            return

        if straight:
            self.hand_name = "straight"
            self.best_cards = straight
            self.hand_val = 4
            return

        if threeofkind:
            self.hand_name = "three of a kind"
            others = self.getothers(threeofkind)
            self.best_cards = threeofkind + others[0:min(2, len(others))]
            self.hand_val = 3
            return

        if twopair:
            self.hand_name = "two pair"
            others = self.getothers(twopair)
            if len(others) != 0:
                self.best_cards = twopair + [others[0]]
            else:
                self.best_cards = twopair
            self.hand_val = 2
            return

        if pair:
            self.hand_name = "pair"
            others = self.getothers(pair)
            self.best_cards = pair + others[0:min(3, len(others))]
            self.hand_val = 1
            return

        self.hand_name = "high card"
        self.best_cards = self.cards[0:min(5, len(self.cards))]
        self.hand_val = 0
            
    #returns pair if there is one
    def pair(self):
        cards = self.cards[:]
        if len(cards) < 2:
            return None
        cur_card = cards[0]
        pair = None
        for card in cards[1:]:
            if cur_card == card:
                pair = [cur_card, card]
                cards.remove(cur_card)
                cards.remove(card)
                return pair
            cur_card = card
        return None

    #returns two pair if there is one
    def twopair(self):
        first_pair = self.pair()
        if first_pair is None or len(self.cards) < 4:
            return None
        cards = self.getothers(first_pair)
        new_hand = PokerHand()
        new_hand.add_cards(cards)
        second_pair = new_hand.pair()
        if second_pair:
            return first_pair + second_pair
        return None

    #returns three of a kind if there is one
    def threeofkind(self):
        cards = self.cards[:]
        if len(cards) < 3:
            return None
        cur_card = cards[0]
        three = None
        for i in range(2, len(cards)):
            if cur_card == cards[i]:
                three = [cur_card, cards[i - 1], cards[i]]
                return three
            cur_card = cards[i - 1]
        return None

    #returns four of a kind if there is one
    def fourofkind(self):
        cards = self.cards[:]
        if len(cards) < 4:
            return None
        cur_card = cards[0]
        four = None
        for i in range(3, len(cards)):
            if cur_card == cards[i]:
                four = [cur_card, cards[i - 2], cards[i - 1], cards[i]]
                return four
            cur_card = cards[i - 2]
        return None

    #returns a straight if there is one
    def straight(self):
        cards = []
        vals = []
        for card in self.cards:
            if card.num_val not in vals:
                cards.append(card)
                vals.append(card.num_val)
        count = 0
        straight = []
        for card in cards:
            if count == 0 or card.num_val + 1 == straight[-1].num_val:
                straight.append(card)
                count += 1
                if count == 5:
                    return straight
            else:
                count = 0
        #checks for low A straight
        if count == 4 and straight[-1].num_val == 2 and cards[0].num_val == 14:
            return straight + cards[0]
        return None

    #only works for hands of less than 10 cards
    #I do not want to order the list of list of card objects
    #too complicated for right now
    #this is fine for the moment, because holdem and theoretically omaha
    def flush(self):
        spades = list(filter(lambda card: (card.suite == "Spades"), self.cards))
        clubs = list(filter(lambda card: (card.suite == "Clubs"), self.cards))
        diamonds = list(filter(lambda card: (card.suite == "Diamonds"), self.cards)) 
        hearts = list(filter(lambda card: (card.suite == "Hearts"), self.cards))
        if len(spades) >= 5:
            return spades[0:5]
        if len(clubs) >= 5:
            return clubs[0:5]
        if len(diamonds) >= 5:
            return diamonds[0:5]
        if len(hearts) >= 5:
            return hearts[0:5]
        return None

    def fullhouse(self):
        if len(self.cards) < 5:
            return None
        three = self.threeofkind()
        if not three:
            return None
        new_hand = PokerHand()
        new_hand.add_cards(self.getothers(three))
        pair = new_hand.pair()
        if pair:
            return three + pair
        return None

    #just like flush it only truly returns the best if the hand is less than 10 cards
    def straightflush(self):
        flush = self.flush()
        if not flush:
            return None
        suite = flush[0].suite
        others = list(filter(lambda card: (card.suite == suite), self.getothers(flush)))
        new_hand = PokerHand()
        new_hand.add_cards(flush + others)
        return new_hand.straight()


    #same as flush and straightflush
    def royal(self):
        flush = self.flush()
        if not flush:
            return None
        if flush[0].value == "A" and flush[-1].value == "10":
            return flush
        return None