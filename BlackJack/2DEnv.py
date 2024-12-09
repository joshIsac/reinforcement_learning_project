import pygame
import os
from Blackjack1 import BlackjackEnv, Card

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Blackjack Game")

# Colors
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Load card images
CARD_WIDTH, CARD_HEIGHT = 100, 150
card_images = {}
card_dir = "D:/GitHub/reinforcement_learning_project/cards"  # Update with the correct path to your card images

for suit in ["clubs", "diamonds", "hearts", "spades"]:
    for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]:
        card_name = f"{rank} of {suit}.jpg"
        card_path = os.path.join(card_dir, card_name)
        card_images[f"{rank} of {suit}"] = pygame.transform.scale(pygame.image.load(card_path), (CARD_WIDTH, CARD_HEIGHT))

# Initialize Blackjack environment
env = BlackjackEnv()

def draw_card(card, x, y):
    """Draw a card on the screen."""
    card_key = f"{card.rank} of {card.suit}"
    screen.blit(card_images[card_key], (x, y))

def draw_hand(hand, x, y):
    """Draw a player's hand."""
    for i, card in enumerate(hand.cards):
        draw_card(card, x + i * 30, y)

def draw_table(player_hand, dealer_hand, dealer_hide_second=False, message=None):
    """Render the table."""
    screen.fill(GREEN)
    if dealer_hide_second:
        draw_card(dealer_hand.cards[0], 300, 50)
        pygame.draw.rect(screen, BLACK, pygame.Rect(330, 50, CARD_WIDTH, CARD_HEIGHT))
    else:
        draw_hand(dealer_hand, 300, 50)
    draw_hand(player_hand, 300, 400)
    
    font = pygame.font.Font(None, 36)
    player_text = font.render(f"Player Value: {player_hand.value()}", True, WHITE)
    screen.blit(player_text, (50, 500))

    if message:
        message_text = font.render(message, True, WHITE)
        screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2))

    # Draw buttons (Hit and Stick)
    hit_button = pygame.Rect(100, 520, 100, 40)
    stick_button = pygame.Rect(600, 520, 100, 40)
    
    pygame.draw.rect(screen, BUTTON_COLOR, hit_button)
    pygame.draw.rect(screen, BUTTON_COLOR, stick_button)
    
    hit_text = font.render("Hit", True, BUTTON_TEXT_COLOR)
    stick_text = font.render("Stick", True, BUTTON_TEXT_COLOR)
    
    screen.blit(hit_text, (hit_button.centerx - hit_text.get_width() // 2, hit_button.centery - hit_text.get_height() // 2))
    screen.blit(stick_text, (stick_button.centerx - stick_text.get_width() // 2, stick_button.centery - stick_text.get_height() // 2))

def check_for_result(player_hand, dealer_hand):
    """Check the result of the game (win/loss/bust)."""
    player_value = player_hand.value()
    dealer_value = dealer_hand.value()

    if player_value > 21:
        return "Player Busted!"
    elif dealer_value > 21:
        return "Dealer Busted!"
    elif player_value > dealer_value:
        return "You Win!"
    elif player_value < dealer_value:
        return "Dealer Wins!"
    else:
        return "It's a Tie!"

def main():
    clock = pygame.time.Clock()
    state = env.reset()
    running = True
    done = False
    message = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not done:
                    if event.key == pygame.K_h:  # Hit
                        state, _, done = env.step(1)
                    elif event.key == pygame.K_s:  # Stick
                        state, _, done = env.step(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not done:
                    mouse_x, mouse_y = event.pos
                    hit_button = pygame.Rect(100, 520, 100, 40)
                    stick_button = pygame.Rect(600, 520, 100, 40)

                    if hit_button.collidepoint(mouse_x, mouse_y):
                        state, _, done = env.step(1)  # Hit
                    elif stick_button.collidepoint(mouse_x, mouse_y):
                        state, _, done = env.step(0)  # Stick

        if done:
            # Check for result after the game ends
            message = check_for_result(env.player_hand, env.dealer_hand)

        draw_table(env.player_hand, env.dealer_hand, dealer_hide_second=not done, message=message)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
