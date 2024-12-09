import random

class Card:
    """Class to represent a single card."""
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value(self):
        """Return the value of the card."""
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11  # Ace can also be 1, but we'll handle that in hand value calculation
        else:
            return int(self.rank)

class Deck:
    """Class to represent a deck of cards."""
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                      for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']]
        random.shuffle(self.cards)

    def draw_card(self):
        """Draw a card from the deck."""
        return self.cards.pop() if self.cards else None

class Hand:
    """Class to represent a player's hand."""
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """Add a card to the hand."""
        self.cards.append(card)

    def value(self):
        """Calculate the total value of the hand."""
        total = sum(card.value() for card in self.cards)
        # Adjust for Aces
        aces = sum(1 for card in self.cards if card.rank == 'Ace')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

class BlackjackGame:
    """Class to represent the Blackjack game."""
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def start_game(self):
        """Start a new game of Blackjack."""
        self.player_hand.add_card(self.deck.draw_card())
        self.player_hand.add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())

        self.player_turn()

    def player_turn(self):
        """Handle the player's turn."""
        while True:
            print(f"Your hand: {[card.rank for card in self.player_hand.cards]} (Value: {self.player_hand.value()})")
            print(f"Dealer's visible card: {self.dealer_hand.cards[0].rank}")

            if self.player_hand.value() > 21:
                print("You bust! Dealer wins.")
                return

            action = input("Choose 'hit' or 'stick': ").lower()
            if action == 'hit':
                self.player_hand.add_card(self.deck.draw_card())
            elif action == 'stick':
                self.dealer_turn()
                return

    def dealer_turn(self):
        """Handle the dealer's turn."""
        while self.dealer_hand.value() < 17:
            self.dealer_hand.add_card(self.deck.draw_card())

        print(f"Dealer's hand: {[card.rank for card in self.dealer_hand.cards]} (Value: {self.dealer_hand.value()})")
        self.determine_winner()

    def determine_winner(self):
        """Determine the winner of the game."""
        player_value = self.player_hand.value()
        dealer_value = self.dealer_hand.value()

        if dealer_value > 21 or player_value > dealer_value:
            print("You win!")
        elif player_value < dealer_value:
            print("Dealer wins!")
        else:
            print("It's a tie!")

# To play the game
if __name__ == "__main__":
    game = BlackjackGame()
    game.start_game()