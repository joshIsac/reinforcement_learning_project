THIS IS A GROUP PROJECT DONE BY JOSHWIN ISAC AND SAI DARSHAN


BLACK JACK:
We all know about the game Black Jack game also known to be 21 a card game where players try to get closer to 21 than the dealer and 

the main goal is 
Players try to have a higher hand value than the dealer without going over 21.
Cards

Face cards (Jack, Queen, King) are worth 10, Aces are worth 1 or 11, and other cards are worth their face value.

Dealing
Players receive two cards face up, and the dealer receives two cards, one face up and one face down. 

Playing
Players can choose to "hit" and receive more cards or "stand" and keep their current hand. 

Winning
If a player's hand is closer to 21 than the dealer's, they win. If the dealer's hand goes over 21, all players win. If neither the player nor the dealer goes over 21, the player with the higher hand wins.

in case there is a tie  
Ties
If neither the player nor the dealer goes over 21, it's a tie, or "push", and the bet remains on the table. 

Blackjack
If a player's first two cards total 21, it's called a "blackjack" or "natural" and is the strongest hand. If a player has a blackjack, their bet is multiplied by 3.


Working of QLEARNING :

## How Q Learning works in Black Jack
As, Q learning is one of the reinforcement learning algorithm where no model is required where it finds the best optimal action selection policy for a finite MDP where it helps an agent to maximize the reward over time through repeated interaction with the environment even though the model is not known 

therefore it is called to be as 
Model-Free Approach where 
No Model Required: Q-learning is a model-free algorithm, which means it does not require a model of the environment (i.e., it does not need to know the transition probabilities and reward functions). This makes it particularly useful in environments where the dynamics are unknown or difficult to model.


Direct Learning from Experience: The agent learns optimal policies directly from interactions with the environment through trial and error without needing to construct or infer a model.



## Working :
In this algorithm it maintains Q values for each state -action pair ,representing the expected utility of taking an given action in a given state following the optimal policy The Q-values are initialized arbitrarily and are updated iteratively using the experiences gathered by the agent.

2. Q-value Update Rule: The Q-values are updated using the formula:

𝑄(𝑠,𝑎)←𝑄(𝑠,𝑎)+𝛼[𝑟+𝛾max𝑎′𝑄(𝑠′,𝑎′)−𝑄(𝑠,𝑎)]

The Q-values are initialized arbitrarily and are updated iteratively using the experiences gathered by the agent.

where :

𝑠 is the current state.

𝑎 is the action taken.

r is the reward received after taking 
action 𝑎 in state 𝑠.

𝑠′ is the new state after action.

𝑎′ is any possible action from the new state 𝑠′.

𝛼 is the learning rate (0 < α ≤ 1).

𝛾 is the discount factor (0 ≤ γ < 1).


defining the policy :
policy determines what action to be taken in each state and that can be derived from the Q values also known to be as Action value of each state ,the policy chooses the action with the highest Q-value in each state (exploitation), though sometimes a less optimal action is chosen for exploration purposes.


4.Exploration vs Exploitation :  Q-learning manages the trade-off between exploration (choosing random actions to discover new strategies) and exploitation (choosing actions based on accumulated knowledge). Techniques like the epsilon-greedy strategy, where the agent mostly takes the best-known action but occasionally tries a random action, often manage the balance between these.


Convergence: Under certain conditions, such as ensuring all state-action pairs are visited an infinite number of times, Q-learning converges to the optimal policy and Q-values that give the maximum expected reward for any state under any conditions.








main game page:

![image](https://github.com/user-attachments/assets/aa449ade-b60a-46db-94c3-eb48f96b3fab)



player Busted :

![image](https://github.com/user-attachments/assets/ce4bcfde-cecf-4114-8822-af6708f87f1d)



dealer win:

![image](https://github.com/user-attachments/assets/d51a1bb5-be50-49b8-a933-b2ce1476da5f)



player wins:

![image](https://github.com/user-attachments/assets/7f6dbd6c-79a9-4711-96e5-c03ba28cfc1f)
