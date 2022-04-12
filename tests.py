import unittest

from poker import card
from poker import deck
from poker import hand
from poker import player

#test cases for the card class
class TestCard(unittest.TestCase):
    def test_constructor(self):
        card1 = card("Spades", "5")
        self.assertEqual(card1.suite, "Spades")
        self.assertEqual(card1.value, "5")
        self.assertEqual(card1.num_val, 5)
        
    def test_error(self):
        with self.assertRaises(ValueError):
            card("Sdfasd", "9")
        with self.assertRaises(ValueError):
            card("Spades", "asdf")

    def test_lt(self):
        card1 = card("Hearts", "9")
        card2 = card("Spades", "K")
        self.assertTrue(card1 < card2)
        self.assertTrue(card2 > card1)

    def test_str(self):
        card1 = card("Clubs", "Q")
        self.assertEqual(str(card1), "Q of Clubs")

class TestDeck(unittest.TestCase):
    def test_constructor(self):
        deck1 = deck()
        self.assertEqual(len(deck1.deck), 52)

    def test_deal(self):
        deck1 = deck()
        card = deck1.deal()
        self.assertEqual(len(deck1.deck), 51)
        self.assertIsNotNone(card)

    def test_burn(self):
        deck1 = deck()
        card = deck1.deal()
        self.assertEqual(len(deck1.deck), 51)
        self.assertIsNotNone(card)
        burn = deck1.burn()
        self.assertEqual(len(deck1.deck), 50)
        self.assertIsNone(burn)

    def test_reshuffle(self):
        deck1 = deck()
        for i in range(30):
            deck1.burn()
        self.assertEqual(len(deck1.deck), 22)
        deck1.shuffle()
        self.assertEqual(len(deck1.deck), 52)

class TestHand(unittest.TestCase):
    def test_constructor(self):
        hand1 = hand()
        self.assertEqual(str(hand1), "\nNo Cards\n")
    
    def test_addCard(self):
        hand1 = hand()
        deck1 = deck()
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
        hand1 = hand()
        cards = [card("Spades", "10"), card("Hearts", "10")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "pair")
        self.assertEqual(hand1.hand_val, 1)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_twoPair(self):
        hand1 = hand()
        #these have to be pre sorted
        cards = [card("Spades", "A"), 
                 card("Hearts", "A"),
                 card("Spades", "10"), 
                 card("Hearts", "10")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "two pair")
        self.assertEqual(hand1.hand_val, 2)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_threeOfKind(self):
        hand1 = hand()
        cards = [card("Spades", "A"), 
                 card("Hearts", "A"),
                 card("Clubs", "A")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "three of a kind")
        self.assertEqual(hand1.hand_val, 3)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_straight(self):
        hand1 = hand()
        cards = [card("Spades", "A"), 
                 card("Hearts", "K"),
                 card("Clubs", "Q"),
                 card("Spades", "J"),
                 card("Clubs", "10")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "straight")
        self.assertEqual(hand1.hand_val, 4)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_flush(self):
        hand1 = hand()
        cards = [card("Spades", "A"), 
                 card("Spades", "Q"),
                 card("Spades", "J"),
                 card("Spades", "10"),
                 card("Spades", "9")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "flush")
        self.assertEqual(hand1.hand_val, 5)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)
    
    def test_fullhouse(self):
        hand1 = hand()
        cards = [card("Spades", "A"), 
                 card("Clubs", "A"),
                 card("Diamonds", "A"),
                 card("Spades", "K"),
                 card("Clubs", "K")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "full house")
        self.assertEqual(hand1.hand_val, 6)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_fourOfKind(self):
        hand1 = hand()
        cards = [card("Spades", "A"), 
                 card("Hearts", "A"),
                 card("Clubs", "A"),
                 card("Diamonds", "A")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "four of a kind")
        self.assertEqual(hand1.hand_val, 7)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_straightflush(self):
        hand1 = hand()
        cards = [card("Spades", "K"), 
                 card("Spades", "Q"),
                 card("Spades", "J"),
                 card("Spades", "10"),
                 card("Spades", "9")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "straight flush")
        self.assertEqual(hand1.hand_val, 8)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_royal(self):
        hand1 = hand()
        cards = [card("Spades", "A"),
                 card("Spades", "K"), 
                 card("Spades", "Q"),
                 card("Spades", "J"),
                 card("Spades", "10")]
        hand1.add_cards(cards)
        hand1.update()
        self.assertEqual(hand1.hand_name, "royal flush")
        self.assertEqual(hand1.hand_val, 9)
        self.assertEqual(hand1.best_cards, cards)
        self.assertEqual(hand1.cards, cards)

    def test_compHand(self):
        hand1 = hand()
        hand1.add_cards([card("Spades", "9"), 
                        card("Hearts", "5"),
                        card("Diamonds", "6"), 
                        card("Clubs", "A"),
                        card("Spades", "Q")])
        hand2 = hand()
        hand1.add_cards([card("Clubs", "9"), 
                        card("Diamonds", "5"),
                        card("Diamonds", "6"), 
                        card("Spades", "A"),
                        card("Clubs", "Q")])
        self.assertEqual(hand1, hand2)

class TestPlayer(unittest.TestCase):
    def test_constructor(self):
        player1 = player("player1", 1000)
        self.assertEqual(player1.name, "player1")
        self.assertEqual(player1.money, 1000)

    def test_hand(self):
        player1 = player("player1", 1000)
        deck1 = deck()
        # for i in range(2):
        #     player1.recieve_deal(deck1.deal())
        # for i in range(5):
        #     player1.update_table(deck1.deal())
        self.assertEqual(str(player1.get_hand()), "\nNo Cards\n")
        

if __name__ == '__main__':
    unittest.main()