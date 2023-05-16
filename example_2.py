import numpy as np

# Define the rewards matrix for the points
rewards = np.array([
    [0, 15, 10, 6, 8],
    [-1, 0, 10, 15, 7],
    [-1, -1, 0, 3, 13],
    [-1, -1, -1, 0, 9],
    [8, 12, -1, -1, 0]
])



# Define the Q matrix
Q = np.zeros([5, 5])

# Define the learning parameters
alpha = 0.8  # learning rate
gamma = 0.95  # discount factor
epsilon = 0.2  # exploration rate

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
    
    # Loop over the steps until all points have been visited and the agent returns to point A
    visited = set()
    while len(visited) < 5:
        # Choose an action using the epsilon-greedy policy
        action = epsilon_greedy_policy(state, epsilon)
        
        # Take the action and observe the next state and reward
        next_state = action
        reward = rewards[state, action]
        
        # Update the Q-value for the current state-action pair
        Q[state, action] = (1 - alpha) * Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state, :]))
        
        # Update the set of visited points
        visited.add(state)
        
        # Set the next state as the current state
        state = next_state
    
    # Set the next state as point A
    state = 0
    
    # Loop over the steps until the agent returns to point A
    while state != 0:
        # Choose an action using the epsilon-greedy policy
        action = epsilon_greedy_policy(state, epsilon)
        
        # Take the action and observe the next state and reward
        next_state = action
        reward = rewards[state, action]
        
        # Update the Q-value for the current state-action pair
        Q[state, action] = (1 - alpha) * Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state, :]))
        
        # Set the next state as the current state
        state = next_state

# Print the learned Q matrix
print(Q)
print(visited)
# Find the optimal path
path = [0]
state = 0
while state != 4:
    action = np.argmax(Q[state, :])
    path.append(action)
    state = action
#path.append(0)
print("Optimal path:", path)
