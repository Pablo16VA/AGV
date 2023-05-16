import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
#%pylab inline
import random

gamma = 1 # discounting rate
rewardSize = -1
gridSize = 4
terminationStates = [[0,0]] #terminationStates = [[0,0], [gridSize-1, gridSize-1]]
actions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
numIterations = 10000

def actionRewardFunction(initialPosition, action):
    
    if initialPosition in terminationStates:
        return initialPosition, 0
    
    reward = rewardSize
    finalPosition = np.array(initialPosition) + np.array(action)
    
    if finalPosition[0] == 2 and finalPosition[1] == 0:
        reward = -10
    if finalPosition[0] == 2 and finalPosition[1] == 1:
        reward = -10    
    if finalPosition[0] == 2 and finalPosition[1] == 2:
        reward = -10
    if finalPosition[0] == 0 and finalPosition[1] == 1:
        reward = -10 
    if finalPosition[0] == 0 and finalPosition[1] == 2:
        reward = -10 
    if finalPosition[0] == 0 and finalPosition[1] == 3:
        reward = -10            

    if -1 in finalPosition or 4 in finalPosition: 
        finalPosition = initialPosition
        
    return finalPosition, reward

valueMap = np.zeros((gridSize, gridSize))
states = [[i, j] for i in range(gridSize) for j in range(gridSize)]
# values of the value function at step 0
valueMap

deltas = []
for it in range(numIterations):
    copyValueMap = np.copy(valueMap)
    deltaState = []
    for state in states:
        weightedRewards = 0
        for action in actions:
            finalPosition, reward = actionRewardFunction(state, action)
            weightedRewards += (1/len(actions))*(reward+(gamma*valueMap[finalPosition[0], finalPosition[1]]))
        deltaState.append(np.abs(copyValueMap[state[0], state[1]]-weightedRewards))
        copyValueMap[state[0], state[1]] = weightedRewards
    deltas.append(deltaState)
    valueMap = copyValueMap
    if it in [0,1,2,500,1000, numIterations-1]: #we can add or change the itteration number that like to see its result
        print("Iteration {}".format(it+1))
        print(valueMap)
        print("")
plt.figure(figsize=(20, 10))
plt.plot(deltas)