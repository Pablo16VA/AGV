import numpy as np

# Define the environment as a 5x5 grid
env_shape = (5, 5)
obstacles = [(1, 1), (2, 2), (3, 1)]
goal = (4, 4)

# Define the action space and set the learning rate and discount factor
action_space = ('up', 'down', 'left', 'right')
learning_rate = 0.1
discount_factor = 0.9

# Initialize the Q-table to zeros
q_table = np.zeros((env_shape[0], env_shape[1], len(action_space)))

# Define a function to choose an action based on the current state
def choose_action(state, epsilon):
    if np.random.uniform(0, 1) < epsilon:
        # Choose a random action
        action = np.random.choice(action_space)
    else:
        # Choose the action with the highest Q-value
        action = action_space[np.argmax(q_table[state])]
    return action

# Define a function to update the Q-value for a given state-action pair
def update_q_value(state, action, reward, next_state):
    max_q_value = np.max(q_table[next_state])
    q_table[state][action_space.index(action)] += learning_rate * \
        (reward + discount_factor * max_q_value - q_table[state][action_space.index(action)])

# Define a function to simulate a single episode of the environment
def run_episode(epsilon):
    state = (0, 0)
    done = False
    total_reward = 0

    while not done:
        # Choose an action based on the current state
        action = choose_action(state, epsilon)

        # Calculate the next state and reward based on the chosen action
        if action == 'up':
            next_state = (max(state[0]-1, 0), state[1])
        elif action == 'down':
            next_state = (min(state[0]+1, env_shape[0]-1), state[1])
        elif action == 'left':
            next_state = (state[0], max(state[1]-1, 0))
        else:
            next_state = (state[0], min(state[1]+1, env_shape[1]-1))

        # Calculate the reward for the next state
        if next_state in obstacles:
            reward = -1
            next_state = state
        elif next_state == goal:
            reward = 1
            done = True
        else:
            reward = 0

        # Update the Q-value for the current state-action pair
        update_q_value(state, action, reward, next_state)

        # Move to the next state
        state = next_state
        total_reward += reward

    return total_reward

# Train the agent using the Q-learning algorithm
num_episodes = 1000
epsilon = 0.1
for i in range(num_episodes):
    episode_reward = run_episode(epsilon)
    if i % 100 == 0:
        print('Episode:', i, 'Total reward:', episode_reward)

# Print the learned Q-table
print('Q-table:')
print(q_table)

# Use the learned Q-table to find the optimal path
state = (0, 0)
path = [state]
while state != goal:
    action = action_space[np.argmax(q_table[state])]
    if action == 'up':
        state = (max(state[0]-1, 0), state[1])
    elif action == 'down':
        state = (min(state[0]+1, env_shape[0]-1), state[1])
    elif action == 'left':
        state = (state[0], max(state[1]-1, 0))
    else:
        state = (state[0], min(state[1]+1, env_shape[1]-1))
    path.append(state)

# Print the optimal path
print('Optimal path:', path)
