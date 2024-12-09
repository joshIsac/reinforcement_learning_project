import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 71
CARD_HEIGHT = 96
GREEN = (34, 139, 34)  # Background color for the blackjack table

# Initialize the Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack Game")

# Load card images
def load_card_images(base_path):
    """Load all card images into a dictionary."""
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    card_images = {}

    for suit in suits:
        for rank in ranks:
            image_path = os.path.join(base_path, suit, f"{rank}_of_{suit}.png")
            try:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
                card_images[f"{rank}_of_{suit}"] = image
            except pygame.error as e:
                print(f"Failed to load {image_path}: {e}")
    return card_images

# Card, Deck, Hand, and Game classes
class Card:
    def __init__(self, rank, suit, image):
        self.rank = rank
        self.suit = suit
        self.image = image

    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        return int(self.rank)

class Deck:
    def __init__(self, card_images):
        self.cards = []
        for suit in ['clubs', 'diamonds', 'hearts', 'spades']:
            for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                key = f"{rank}_of_{suit}"
                if key in card_images:
                    self.cards.append(Card(rank, suit, card_images[key]))
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def value(self):
        total = sum(card.value() for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def display(self, x, y):
        for card in self.cards:
            screen.blit(card.image, (x, y))
            x += CARD_WIDTH + 20

class BlackjackGame:
    def __init__(self, card_images):
        self.deck = Deck(card_images)
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.card_images = card_images
        self.game_over = False

    def start_game(self):
        """Start the game, deal initial cards to player and dealer."""
        self.player_hand.add_card(self.deck.draw_card())
        self.player_hand.add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())

    def run(self):
        """Main game loop."""
        self.start_game()

        running = True
        while running:
            screen.fill(GREEN)

            # Display hands
            self.player_hand.display(50, 400)  # Player's hand
            screen.blit(self.card_images['back'], (50, 50))  # Dealer's hidden card
            for i, card in enumerate(self.dealer_hand.cards[1:]):
                screen.blit(card.image, (50 + (i + 1) * (CARD_WIDTH + 20), 50))

            # Display player's hand value
            font = pygame.font.SysFont(None, 36)
            player_value_text = font.render(f"Your Hand Value: {self.player_hand.value()}", True, (255, 255, 255))
            screen.blit(player_value_text, (50, 350))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:  # 'H' for hit
                        self.player_hand.add_card(self.deck.draw_card())
                        if self.player_hand.value() > 21:
                            print("You bust! Dealer wins.")
                            running = False
                    elif event.key == pygame.K_s:  # 'S' for stick
                        while self.dealer_hand.value() < 17:
                            self.dealer_hand.add_card(self.deck.draw_card())
                        self.determine_winner()
                        running = False

            # Check for game over condition
            if self.game_over:
                running = False

        pygame.quit()

    def determine_winner(self):
        """Determine who wins the game."""
        player_value = self.player_hand.value()
        dealer_value = self.dealer_hand.value()
        print(f"Player Value: {player_value}, Dealer Value: {dealer_value}")
        if dealer_value > 21 or player_value > dealer_value:
            print("You win!")
        elif player_value < dealer_value:
            print("Dealer wins!")
        else:
            print("It's a tie!")

# Main execution
if __name__ == "__main__":
    # Define the path to your card images
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "REINFORCEMENT_LEARNING", "BlackJack")

    # Load images
    card_images = load_card_images(base_path)

    # Add a card back image for hidden dealer cards
    back_path = os.path.join(base_path, "back.png")  # Ensure you have a 'back.png' image for the card back
    try:
        card_images['back'] = pygame.image.load(back_path)
        card_images['back'] = pygame.transform.scale(card_images['back'], (CARD_WIDTH, CARD_HEIGHT))
    except pygame.error as e:
        print(f"Failed to load card back image: {e}")

    # Start the game
    game = BlackjackGame(card_images)
    game.run()
