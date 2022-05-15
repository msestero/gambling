from cards.deck import Deck, PokerCard

#This is the hand object
#Each player will have a hand
class hand:

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
        print("here")
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
        new_hand = hand()
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
        new_hand = hand()
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
        new_hand = hand()
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
        

class player:

    def __init__(self, name, starting_money):
        self.name = name
        self.personal_cards = []
        self.table_cards = []
        self.hand = hand()
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

class game:

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
