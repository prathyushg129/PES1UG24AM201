
from cards import Deck, hand_value, is_blackjack


class Blackjack:
    def __init__(self):
        self.chips = 100

    def show(self, player, dealer, hide=True):
        """Display the player's hand and the dealer's visible cards."""
        if hide:
            dealer_cards = (
                f"{dealer[0][0]}{dealer[0][1]} ??"
                if dealer else "No cards"
            )
        else:
            dealer_cards = " ".join(
                f"{rank}{suit}" for rank, suit in dealer
            )

        player_cards = " ".join(
            f"{rank}{suit}" for rank, suit in player
        )

        print(f"\nDealer: {dealer_cards}")
        print(f"Player: {player_cards} = {hand_value(player)}")
        print(f"Chips: {self.chips}")

    def get_wager(self):
        """Ask for a valid wager without changing the chip balance."""
        while True:
            print(f"\nAvailable chips: {self.chips}")
            raw = input("Enter your wager (or q to quit): ").strip().lower()

            if raw == "q":
                return None

            try:
                wager = int(raw)
            except ValueError:
                print("Invalid input. Enter a whole number.")
                continue

            if wager <= 0:
                print("Your wager must be greater than zero.")
            elif wager > self.chips:
                print("You cannot wager more chips than you have.")
            else:
                return wager

    def settle(self, result, wager):
        """Settle a round exactly once."""
        if result == "win":
            self.chips += wager * 2
            print(f"You win! Payout: {wager}.")
        elif result == "lose":
            print(f"You lose your wager of {wager} chips.")
        elif result == "push":
            self.chips += wager
            print("Push! Your wager is returned.")

        print(f"Chip balance: {self.chips}")

    def round(self):
        wager = self.get_wager()

        if wager is None:
            return False

        # Reserve the wager before the cards are dealt.
        self.chips -= wager
        deck = Deck()

        player = [deck.draw(), deck.draw()]
        dealer = [deck.draw(), deck.draw()]

        if any(card is None for card in player + dealer):
            self.chips += wager
            print("Could not deal the cards. Wager refunded.")
            return True

        self.show(player, dealer)

        player_natural = is_blackjack(player)
        dealer_natural = is_blackjack(dealer)

        # Resolve natural Blackjack before any further player actions.
        if player_natural or dealer_natural:
            self.show(player, dealer, hide=False)

            if player_natural and dealer_natural:
                self.settle("push", wager)
            elif player_natural:
                self.settle("win", wager)
                print("Natural Blackjack!")
            else:
                self.settle("lose", wager)
                print("Dealer has natural Blackjack!")

            return True

        # Player's turn.
        while True:
            total = hand_value(player)

            if total >= 21:
                break

            key = input("[h]it, [s]tand, [q]uit: ").strip().lower()

            if key == "q":
                self.chips += wager
                print("Round cancelled. Wager refunded.")
                return False

            elif key == "s":
                break

            elif key == "h":
                card = deck.draw()

                if card is None:
                    print("Deck is empty. Your turn ends.")
                    break

                player.append(card)
                print(f"You drew: {card[0]}{card[1]}")
                self.show(player, dealer)

                if hand_value(player) > 21:
                    print("Bust! Your hand exceeds 21.")
                    self.settle("lose", wager)
                    return True

            else:
                print("Invalid command. Enter h, s, or q.")

        # Dealer's turn.
        while hand_value(dealer) < 17:
            card = deck.draw()

            if card is None:
                print("Deck is empty. Dealer cannot draw.")
                break

            dealer.append(card)
            print(f"Dealer drew: {card[0]}{card[1]}")

        self.show(player, dealer, hide=False)

        player_total = hand_value(player)
        dealer_total = hand_value(dealer)

        if dealer_total > 21:
            print("Dealer busts!")
            self.settle("win", wager)
        elif player_total > dealer_total:
            self.settle("win", wager)
        elif player_total < dealer_total:
            self.settle("lose", wager)
        else:
            self.settle("push", wager)

        return True

    def run(self):
        print("=" * 35)
        print("BLACKJACK VS DEALER")
        print("=" * 35)
        print(f"Starting chips: {self.chips}")

        while self.chips > 0:
            if not self.round():
                break

            if self.chips <= 0:
                print("You have run out of chips!")
                break

            again = input("\nPlay another round? [y/n]: ").strip().lower()

            while again not in {"y", "n"}:
                print("Invalid command. Enter y or n.")
                again = input("Play another round? [y/n]: ").strip().lower()

            if again == "n":
                break

        print(f"\nGame over. Final chips: {self.chips}")
        print("Thanks for playing!")
