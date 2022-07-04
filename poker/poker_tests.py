#change a lot of code this needs to be updated,
#all of them fail right now


import unittest

from cards.deck import Card, Deck, PokerCard
from .poker_hand import PokerHand
from .poker_player import PokerPlayer
from .poker_game import PokerGame

#test cases for the card class
class TestCard(unittest.TestCase):

    def test_constructor(self):
        card1 = PokerCard("Spades", "5")
        self.assertEqual(card1.suite, "Spades")
        self.assertEqual(card1.value, "5")
        self.assertEqual(card1.num_val, 5)
        
    def test_error(self):
        with self.assertRaises(ValueError):
            PokerCard("Sdfasd", "9")
        with self.assertRaises(ValueError):
            PokerCard("Spades", "asdf")

    def test_lt(self):
        card1 = PokerCard("Hearts", "9")
        card2 = PokerCard("Spades", "K")
        self.assertTrue(card1 < card2)
        self.assertTrue(card2 > card1)

    def test_str(self):
        card1 = Card("Clubs", "Q")
        self.assertEqual(str(card1), "Q of Clubs")

class TestDeck(unittest.TestCase):
    def test_constructor(self):
        deck1 = Deck(PokerCard)
        self.assertEqual(len(deck1.deck), 52)

    def test_deal(self):
        deck1 = Deck(PokerCard)
        card = deck1.deal()
        self.assertEqual(len(deck1.deck), 51)
        self.assertIsNotNone(card)

    def test_burn(self):
        deck1 = Deck(PokerCard)
        card = deck1.deal()
        self.assertEqual(len(deck1.deck), 51)
        self.assertIsNotNone(card)
        burn = deck1.burn()
        self.assertEqual(len(deck1.deck), 50)
        self.assertIsNone(burn)

    def test_reshuffle(self):
        deck1 = Deck(PokerCard)
        for i in range(30):
            deck1.burn()
        self.assertEqual(len(deck1.deck), 22)
        deck1.shuffle()
        self.assertEqual(len(deck1.deck), 52)

class TestHand(unittest.TestCase):
    def test_constructor(self):
        hand1 = PokerHand()
        self.assertEqual(str(hand1), "\nNo Cards\n")
    
    def test_addCard(self):
        hand1 = PokerHand()
        deck1 = Deck(PokerCard)
        hand1.add_card(deck1.deal())
        self.assertEqual(hand1.hand_name, None)
        self.assertEqual(hand1.hand_val, 0)
        self.assertEqual(len(hand1.best_cards), 0)
        self.assertEqual(len(hand1.cards), 1)
        hand1.update()
        self.assertEqual(hand1.hand_name, "high card")
        self.assertEqual(hand1.hand_val, 0)
        self.assertEqual(len(hand1.best_cards), 1)
        self.assertEqual(len(hand1.cards), 1)

    def test_pair(self):
        hand1 = PokerHand()
        cards = [PokerCard("Spades", "10"), PokerCard("Hearts", "10")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "pair")
        self.assertEqual(hand1.hand_val, 1)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_twoPair(self):
        hand1 = PokerHand()
        #these have to be pre sorted
        cards = [PokerCard("Spades", "A"), 
                 PokerCard("Hearts", "A"),
                 PokerCard("Spades", "10"), 
                 PokerCard("Hearts", "10")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "two pair")
        self.assertEqual(hand1.hand_val, 2)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_threeOfKind(self):
        hand1 = PokerHand()
        cards = [PokerCard("Spades", "A"), 
                 PokerCard("Hearts", "A"),
                 PokerCard("Clubs", "A")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "three of a kind")
        self.assertEqual(hand1.hand_val, 3)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_straight(self):
        hand1 = PokerHand()
        cards = [PokerCard("Spades", "A"), 
                 PokerCard("Hearts", "K"),
                 PokerCard("Clubs", "Q"),
                 PokerCard("Spades", "J"),
                 PokerCard("Clubs", "10")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "straight")
        self.assertEqual(hand1.hand_val, 4)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_flush(self):
        hand1 = PokerHand()
        cards = [PokerCard("Spades", "A"), 
                 PokerCard("Spades", "Q"),
                 PokerCard("Spades", "J"),
                 PokerCard("Spades", "10"),
                 PokerCard("Spades", "9")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "flush")
        self.assertEqual(hand1.hand_val, 5)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)
    
    def test_fullhouse(self):
        hand1 = PokerHand()
        cards = [PokerCard("Spades", "A"), 
                 PokerCard("Clubs", "A"),
                 PokerCard("Diamonds", "A"),
                 PokerCard("Spades", "K"),
                 PokerCard("Clubs", "K")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "full house")
        self.assertEqual(hand1.hand_val, 6)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_fourOfKind(self):
        hand1 = PokerHand()
        cards = [PokerCard("Spades", "A"), 
                 PokerCard("Hearts", "A"),
                 PokerCard("Clubs", "A"),
                 PokerCard("Diamonds", "A")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "four of a kind")
        self.assertEqual(hand1.hand_val, 7)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_straightflush(self):
        hand1 = PokerHand()
        cards = [PokerCard("Spades", "K"), 
                 PokerCard("Spades", "Q"),
                 PokerCard("Spades", "J"),
                 PokerCard("Spades", "10"),
                 PokerCard("Spades", "9")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "straight flush")
        self.assertEqual(hand1.hand_val, 8)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_royal(self):
        hand1 = PokerHand()
        cards = [PokerCard("Spades", "A"),
                 PokerCard("Spades", "K"), 
                 PokerCard("Spades", "Q"),
                 PokerCard("Spades", "J"),
                 PokerCard("Spades", "10")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "royal flush")
        self.assertEqual(hand1.hand_val, 9)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_compHand(self):
        hand1 = PokerHand()
        hand1.add_cards([PokerCard("Spades", "9"), 
                        PokerCard("Hearts", "5"),
                        PokerCard("Diamonds", "6"), 
                        PokerCard("Clubs", "A"),
                        PokerCard("Spades", "Q")])
        hand2 = PokerHand()
        hand1.add_cards([PokerCard("Clubs", "9"), 
                        PokerCard("Diamonds", "5"),
                        PokerCard("Diamonds", "6"), 
                        PokerCard("Spades", "A"),
                        PokerCard("Clubs", "Q")])
        self.assertEqual(hand1, hand2)

class TestPlayer(unittest.TestCase):
    def test_constructor(self):
        player1 = PokerPlayer("player1", 1000)
        self.assertEqual(player1.name, "player1")
        self.assertEqual(player1.money, 1000)

    def test_hand(self):
        player1 = PokerPlayer("player1", 1000)
        deck1 = Deck(PokerCard)
        # for i in range(2):
        #     player1.recieve_deal(deck1.deal())
        # for i in range(5):
        #     player1.update_table(deck1.deal())
        self.assertEqual(str(player1.get_hand()), "\nNo Cards\n")
        

if __name__ == '__main__':
    unittest.main()