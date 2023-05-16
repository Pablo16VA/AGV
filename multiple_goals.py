import gym
import numpy as np
goal_states = [(2,2), (3,3), (4,4)]
def q_learning(env, num_episodes, alpha, gamma, epsilon, goal_state):
    Q = np.zeros((env.observation_space.n, env.action_space.n))
    episode_rewards = []
    goals_reached = set()
    for episode in range(num_episodes):
        state = env.reset()
        episode_reward = 0
        done = False
        while not done:
            if np.random.rand() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(Q[state])
            next_state, reward, done, info = env.step(action)
            episode_reward += reward
            if next_state in goal_states and next_state not in goals_reached:
                goals_reached.add(next_state)
            Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
            state = next_state
        episode_rewards.append(episode_reward)
        if len(goals_reached) == len(goal_states):
            break
    return Q, episode_rewards

if __name__ == '__main__':
    env = gym.make('FrozenLake-v1', is_slippery=False)
    num_episodes = 10000
    alpha = 0.8
    gamma = 0.95
    epsilon = 0.1
    goal_states = [(2,2), (3,3), (4,4)]

    for goal_state in goal_states:
        Q, episode_rewards = q_learning(env, num_episodes, alpha, gamma, epsilon, goal_states)
        print(f"Q-Table for goal state {goal_state}:")
        print(Q)
        print(f"Episode Rewards for goal state {goal_state}:")
        print(episode_rewards)
