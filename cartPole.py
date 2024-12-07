import gym
import numpy as np
import matplotlib.pyplot as plt

class MountainCarAgent:
    def __init__(self, env):
        self.env = env
        self.q_table = np.zeros((20, 20, env.action_space.n))  # Discretized state space
        self.learning_rate = 0.1
        self.discount_factor = 0.99
        self.exploration_rate = 1.0
        self.exploration_decay = 0.995
        self.min_exploration_rate = 0.01

    def discretize_state(self, state):
        position, velocity = state
        pos_bins = np.linspace(-1.2, 0.6, 20)
        vel_bins = np.linspace(-0.07, 0.07, 20)
        pos_index = np.digitize(position, pos_bins) - 1
        vel_index = np.digitize(velocity, vel_bins) - 1
        return pos_index, vel_index

    def choose_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return self.env.action_space.sample()  # Explore
        else:
            pos_index, vel_index = self.discretize_state(state)
            return np.argmax(self.q_table[pos_index, vel_index])  # Exploit

    def update_q_table(self, state, action, reward, next_state):
        pos_index, vel_index = self.discretize_state(state)
        next_pos_index, next_vel_index = self.discretize_state(next_state)
        best_next_action = np.argmax(self.q_table[next_pos_index, next_vel_index])
        td_target = reward + self.discount_factor * self.q_table[next_pos_index, next_vel_index, best_next_action]
        td_delta = td_target - self.q_table[pos_index, vel_index, action]
        self.q_table[pos_index, vel_index, action] += self.learning_rate * td_delta

    def train(self, episodes):
        rewards = []
        for episode in range(episodes):
            state = self.env.reset()
            total_reward = 0
            done = False

            while not done:
                action = self.choose_action(state)
                next_state, reward, done, _ = self.env.step(action)
                self.update_q_table(state, action, reward, next_state)
                state = next_state
                total_reward += reward

            rewards.append(total_reward)
            self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
            print(f'Episode: {episode}, Total Reward: {total_reward}')

        return rewards

def main():
    env = gym.make('MountainCar-v0')
    agent = MountainCarAgent(env)
    episodes = 1000
    rewards = agent.train(episodes)

    plt.plot(rewards)
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.title('Total Reward per Episode in Mountain Car')
    plt.show()

    env.close()

if __name__ == "__main__":
    main()