
import random

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["C", "D", "H", "S"]


class Deck:
    def __init__(self):
        self.cards = [
            (rank, suit)
            for suit in SUITS
            for rank in RANKS
        ]
        random.shuffle(self.cards)

    def draw(self):
        """Draw one card, or return None if the deck is empty."""
        if not self.cards:
            return None
        return self.cards.pop()


def hand_value(hand):
    """Calculate a Blackjack hand total with correct Ace scoring."""
    total = 0
    aces = 0

    for rank, suit in hand:
        if rank == "A":
            total += 11
            aces += 1
        elif rank in {"J", "Q", "K"}:
            total += 10
        else:
            total += int(rank)

    # Convert Aces from 11 to 1 when the hand would bust.
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


def is_blackjack(hand):
    """A natural Blackjack is exactly two cards totaling 21."""
    return len(hand) == 2 and hand_value(hand) == 21
