
import unittest

from cards import Deck, hand_value, is_blackjack


class TestBlackjackCards(unittest.TestCase):

    def test_ace_and_nine(self):
        self.assertEqual(
            hand_value([("A", "S"), ("9", "H")]), 20
        )

    def test_ace_nine_five(self):
        self.assertEqual(
            hand_value([
                ("A", "S"), ("9", "H"), ("5", "D")
            ]), 15
        )

    def test_two_aces_and_nine(self):
        self.assertEqual(
            hand_value([
                ("A", "S"), ("A", "H"), ("9", "D")
            ]), 21
        )

    def test_face_cards(self):
        self.assertEqual(
            hand_value([("K", "S"), ("Q", "H")]), 20
        )

    def test_natural_blackjack(self):
        self.assertTrue(
            is_blackjack([("A", "S"), ("K", "H")])
        )

    def test_three_card_21_is_not_natural(self):
        self.assertFalse(
            is_blackjack([
                ("7", "S"), ("7", "H"), ("7", "D")
            ])
        )

    def test_deck_has_52_cards(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)
        self.assertEqual(len(set(deck.cards)), 52)

    def test_empty_deck(self):
        deck = Deck()
        deck.cards.clear()
        self.assertIsNone(deck.draw())


if __name__ == "__main__":
    unittest.main()
