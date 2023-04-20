import numpy as np
from visualization import *
from cube import *
import time
import sys


# so we can run one agent first
def updateAgent(agent):
    old = agent.position
    agent.position = runPolicy(agent.algo, agent)  # will get next move base on policy

    action_result = perform_cell_action(agent.carrying_block, agent.position)  # x.q_table[:-1] as arg 2
    agent.carrying_block = action_result[0]
    reward = action_result[1]
    updateAgentRewards(agent, reward)
    updatePositionFrequency(agent)

    updateQTable(agent, old, reward)  # change depending on how q_table works
    # space for updating q_table
    # might shrink parameters to just agent, depending on how q_table is done


iterations = 5000


def train(cube):
    # for loop for num of iterations?
    goal_reached = 0
    for i in range(iterations):
        for agent in agents:
            time.sleep(.05)
            rate(60)
            updateAgent(agents[agent])
            cube.draw_agents(agents.values())
            if checkTerminalState():
                goal_reached += 1
                initializeCube()

    return goal_reached


# maybe a return q_table of agents and reset agents so we can check the train with multiple policies
def initializeCube():
    cube.clear()

    for i in pickups:
        addCell(i, CellType.pickupCell, pickup_reward, pickup_capacity, pickup_capacity)

    for i in dropoffs:
        addCell(i, CellType.dropoffCell, dropoff_reward, dropoff_capacity, 0)

    for i in risks:
        addCell(i, CellType.riskyCell, risk_reward)

    # adds normal cells
    for i in all_cells:
        addCell(i, reward=action_cost)


def addPositionFrequency(agent):
    agent.frequencyTable = np.zeros((length, height, depth))


def updatePositionFrequency(agent):
    x, y, z = agent.position
    agent.frequencyTable[x - 1][y - 1][z - 1] += 1


def addAgentRewards(agent):
    agent.rewards = 0


def updateAgentRewards(agent, reward):
    agent.rewards += reward


def addPathTaken(agent):
    agent.path = []


def test():
    for agent in agents:
        addPathTaken(agents[agent])
    i = 0
    while not checkTerminalState() and i < iterations:
        for agent in agents:
            updateAgent(agents[agent])
            agents[agent].path.append(agents[agent].position)
        i += 1


def trainForPolicy(func):
    agents.clear()
    initializeCube()
    makeAgent('x', (1, 1, 1), func)
    makeAgent('y', (2, 3, 3), func)
    addPositionFrequency(agents['x'])
    addPositionFrequency(agents['y'])
    addAgentRewards(agents['x'])
    addAgentRewards(agents['y'])

    visual = cube_visualized(3, 1, list(agents.values()))
    visual.draw_cubes(pickups, dropoffs, risks)

    print('train results')
    print('Goals: ', train(visual))
    for agent in agents:
        print(agent)
        print('Rewards:', agents[agent].rewards)
        print()
        #print(agents[agent].frequencyTable)
    print()
    test()
    print('Test Path')
    if agents['x'].path[0] == agents['x'].path[2] and agents['x'].path[1] == agents['x'].path[3]:
        print('looping')
    else:
        print('     x: ', agents['x'].path)
        print('     y: ', agents['y'].path)
    print()
    visual.invisible(agents.values())


trainForPolicy(PRANDOM)
trainForPolicy(PEXPLOIT)
trainForPolicy(PGREEDY)

done()