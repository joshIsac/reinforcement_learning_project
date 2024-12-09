import random
import numpy as np

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

    def usable_ace(self):
        """Check if the hand has a usable Ace."""
        return any(card.rank == 'Ace' for card in self.cards) and self.value() + 10 <= 21

class BlackjackEnv:
    """Class to represent the Blackjack environment."""
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def reset(self):
        """Reset the environment for a new game."""
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.player_hand.add_card(self.deck.draw_card())
        self.player_hand.add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())

        return self.get_state()

    def get_state(self):
        """Return the current state of the game."""
        player_value = self.player_hand.value()
        dealer_visible_card = self.dealer_hand.cards[0].value()
        usable_ace = self.player_hand.usable_ace()
        return (player_value, dealer_visible_card, usable_ace)

    def step(self, action):
        """Take an action in the environment."""
        if action == 1:  # Hit
            self.player_hand.add_card(self.deck.draw_card())
            if self.player_hand.value() > 21:  # Player busts
                print("Player busts!")
                return self.get_state(), -1, True  # Lose
             
        else:  # Stick
            while self.dealer_hand.value() < 17:
                print("Dealer hits.")
                self.dealer_hand.add_card(self.deck.draw_card())

            # Determine the winner
            player_value = self.player_hand.value()
            dealer_value = self.dealer_hand.value()

            if dealer_value > 21 or player_value > dealer_value:
                print("Player wins!")
                return self.get_state(), 1, True  # Win
            
            elif player_value < dealer_value:
                print("Dealer wins!")
                return self.get_state(), -1, True  # Lose
            else:
                return self.get_state(), 0, True  # Draw

        return self.get_state(), -0.1, False  # Intermediate step penalty

# Q-Learning implementation
def q_learning(num_episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
    """Train an agent to play Blackjack using Q-Learning."""
    env = BlackjackEnv()
    q_table = np.zeros((32, 10, 2, 2))  # (Player value, Dealer card [2-11], Usable Ace, Actions)

    for episode in range(num_episodes):
        state = env.reset()
        done = False

        while not done:
            player_value, dealer_visible_card, usable_ace = state
            dealer_idx = dealer_visible_card - 2
            state_idx = (min(player_value, 21), dealer_idx, int(usable_ace))
            
            # Epsilon-greedy action selection
            if random.uniform(0, 1) < epsilon:
                action = random.choice([0, 1])  # Explore
            else:
                action = np.argmax(q_table[state_idx])  # Exploit

            next_state, reward, done = env.step(action)
            next_player_value, next_dealer_visible_card, next_usable_ace = next_state
            next_dealer_idx = next_dealer_visible_card - 2
            next_state_idx = (min(next_player_value, 21), next_dealer_idx, int(next_usable_ace))

            # Q-value update
            q_table[state_idx][action] += alpha * (
                reward + gamma * np.max(q_table[next_state_idx]) - q_table[state_idx][action]
            )

            state = next_state

        # Print progress every 100 episodes
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}/{num_episodes} complete.")

    return q_table

def play_user_vs_dealer():
    """Let the user play against the dealer."""
    env = BlackjackEnv()
    state = env.reset()
    done = False
    print("\nStarting a new game of Blackjack!")

    while not done:
        print(f"\nYour hand: {[(card.rank, card.suit) for card in env.player_hand.cards]}, Value: {env.player_hand.value()}")
        print(f"Dealer's visible card: {env.dealer_hand.cards[0].rank} of {env.dealer_hand.cards[0].suit}")
        
        action = input("Enter 'h' to hit or 's' to stick: ").strip().lower()
        action = 1 if action == 'h' else 0

        state, reward, done = env.step(action)

        if done:
            print(f"\nYour final hand: {[(card.rank, card.suit) for card in env.player_hand.cards]}, Value: {env.player_hand.value()}")
            print(f"Dealer's final hand: {[(card.rank, card.suit) for card in env.dealer_hand.cards]}, Value: {env.dealer_hand.value()}")
            if reward > 0:
                print("You win!")
            elif reward < 0:
                print("Dealer wins!")
            else:
                print("It's a tie!")
            print("Game Over.\n")

# Main Program
if __name__ == "__main__":
    print("Training the agent using Q-learning...")
    q_table = q_learning(num_episodes=1000)
    print("Training complete!\n")

    # Let the user play 3 games against the dealer
    for _ in range(3):
        play_user_vs_dealer()
