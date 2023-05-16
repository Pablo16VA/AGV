import numpy as np

# Define the rewards matrix for the points
rewards = np.array([
    [0, 15, 10, 6, 8],  #A rewards
    [7, 0, 10, 15, 7], #B rewards
    [10, 7, 0, 3, 13],  #C rewards
    [2, 5, 3, 0, 9],   #D rewards
    [8, 6, 9, 8, 0]     #E rewards
])

# Define the Q matrix
Q = np.zeros([5, 5])

# Define the learning parameters
alpha = 0.9  # learning rate
gamma = 0.95  # discount factor
epsilon = 0.1  # exploration rate

# Define the epsilon-greedy policy function
def epsilon_greedy_policy(state, epsilon):
    if np.random.uniform(0, 1) < epsilon:
        # exploration
        action = np.random.choice(5)
    else:
        # exploitation
        action = np.argmax(Q[state, :])
    return action

# Train the Q-learning algorithm
for episode in range(1000):
    # Reset the starting state to point A
    state = 0
    visited = set()
    # Loop over the steps until the goal state (point E) is reached
    while len(visited) < 5:
        # Choose an action using the epsilon-greedy policy
        action = epsilon_greedy_policy(state, epsilon)
        
        # Take the action and observe the next state and reward
        next_state = action
        reward = rewards[state, action]
        
        # Update the Q-value for the current state-action pair
        Q[state, action] = (1 - alpha) * Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state, :]))
        
        # Set the next state as the current state
        state = next_state

        #Update states visited
        visited.add(state)

# Print the learned Q matrix
print(Q)

# Find the optimal path
path = [0]
state = 0
visited = set()
while len(visited)< 4:
    action = np.argmax(Q[state, :])
    path.append(action)
    state = action
    visited.add(state)
print("Optimal path:", path)

