from enum import Enum, auto
import random
import numpy as np

cube = {}
agents = {}
actions = {(1, 0, 0): 'East', (-1, 0, 0): 'West',
           (0, 1, 0): 'North', (0, -1, 0): 'South',
           (0, 0, 1): 'Up', (0, 0, -1): 'Down'}
action_cost = -1
alpha = 0.3
gamma = 0.5
pickups = [(2, 2, 1), (3, 3, 2)]
pickup_reward = 14
pickup_capacity = 10
dropoffs = [(1, 1, 2), (1, 1, 3), (3, 1, 1), (3, 2, 3)]
dropoff_reward = 14
dropoff_capacity = 5
risks = [(2, 2, 2), (3, 2, 1)]
risk_reward = 2 * action_cost

all_cells = []
length = 3
height = 3
depth = 3
for x in range(1, length + 1):
    for y in range(1, height + 1):
        for z in range(1, depth + 1):
            all_cells.append((x, y, z))


class CellType(Enum):
    normalCell = auto()
    riskyCell = auto()
    pickupCell = auto()
    dropoffCell = auto()


class Cell:
    cellType = CellType.normalCell
    position = (0, 0, 0)
    reward = 0
    max_capacity = 0
    holding = 0


class Agent:
    position = (1, 1, 1)
    q_table = []
    carrying_block = False
    algo = None


def addCell(position, ctype=CellType.normalCell, reward=0, capacity=0, holding=0):
    if position not in cube:
        cell = Cell()
        cell.cellType = ctype
        cell.position = position
        cell.reward = reward
        cell.max_capacity = capacity
        cell.holding = holding
        cube.update({position: cell})


def checkMoves(position, agent_actions=actions.keys()):
    moves = []
    east_west, north_south, up_down = position
    offsets = agent_actions

    for dx, dy, dz in offsets:
        if 0 < east_west + dx < 4 and 0 < north_south + dy < 4 and 0 < up_down + dz < 4:
            moves.append((east_west + dx, north_south + dy, up_down + dz))

    return moves


def findCellTypeInReach(position, c_type):
    next_position = checkMoves(position)
    cells = [place for place in next_position if cube[place].cellType == c_type]
    return cells


# actions
def perform_cell_action(carry, position):
    if cube[position].cellType == CellType.normalCell or cube[position].cellType == CellType.riskyCell:
        return carry, cube[position].reward

    if cube[position].cellType == CellType.pickupCell:
        return pickup(carry, position)

    if cube[position].cellType == CellType.dropoffCell:
        return dropoff(carry, position)


def pickup(carry, position):
    if not carry and cube[position].holding - 1 > -1:
        cube[position].holding -= 1
        return True, cube[position].reward

    return carry, cube[position].reward


def dropoff(carry, position):
    if carry and cube[position].holding + 1 <= cube[position].max_capacity:
        cube[position].holding += 1
        return False, cube[position].reward

    return carry, cube[position].reward


# checks if any agent in spot
def checkCollision(position):
    for agent in agents:
        if agents[agent].position == position:
            return True
    return False


def runPolicy(function, agent):
    return function(agent)


# returns list of positions where action is applicable
def isPickupApplicable(position, carry):
    if carry:
        return []

    nearby = findCellTypeInReach(position, CellType.pickupCell)
    have_items = [cell for cell in nearby if cube[cell].holding - 1 > -1]

    return have_items


def isDropoffApplicable(position, carry):
    if not carry:
        return []

    nearby = findCellTypeInReach(position, CellType.dropoffCell)
    have_space = [cell for cell in nearby if cube[cell].holding + 1 <= cube[cell].max_capacity]

    return have_space


# policies
# this one was changed for a test
# def getPostionFromTable(index):
#     return list(cube.keys())[index]
# print(np.argmax(agents['y'].q_table))


def PRANDOM(agent):
    # Check if pickup and dropoff are applicable
    nextPosition = isDropoffApplicable(agent.position, agent.carrying_block) + \
                   isPickupApplicable(agent.position, agent.carrying_block)

    if nextPosition:
        return random.choice(nextPosition)
    # If not, choose an applicable operator randomly
    applicable_actions = [position for position in checkMoves(agent.position) if not checkCollision(position)]

    return random.choice(applicable_actions)


def getMaxQForPositions(positions, agent):
    values = []
    state_index = list(cube.keys()).index(agent.position)

    for new_position in positions:
        move = getMove(agent.position, new_position)
        action_index = list(actions.keys()).index(move)

        values.append(agent.q_table[state_index][action_index])

    return max(values)


def getBestActions(positions, agent):
    max_q_value = getMaxQForPositions(positions, agent)
    best_actions = []

    for new_position in positions:
        move = getMove(agent.position, new_position)
        action_index = list(actions.keys()).index(move)
        position_index = list(cube.keys()).index(agent.position)

        if agent.q_table[position_index][action_index] == max_q_value:
            best_actions.append(new_position)

    return best_actions


# to be changed later
def PEXPLOIT(agent):
    # Check if pickup and dropoff are applicable
    nextPosition = isDropoffApplicable(agent.position, agent.carrying_block) + \
                   isPickupApplicable(agent.position, agent.carrying_block)

    if nextPosition:
        return random.choice(nextPosition)
    # If not, choose the applicable operator with highest q-value
    applicable_positions = [position for position in checkMoves(agent.position) if not checkCollision(position)]
    # max_q_value = max([q_matrix[state][action] for action in applicable_actions])

    # best_actions = [action for action in applicable_actions if q_matrix[state][action] == max_q_value]
    # # If there is only one best action, choose it with probability 0.85
    best_actions = getBestActions(applicable_positions, agent)

    if len(best_actions) == 1:
        return best_actions[0] if random.uniform(0, 1) < 0.85 else random.choice(applicable_positions)
    # If there are multiple best actions, choose one of them with probability 0.85
    else:
        return random.choice(best_actions) if random.uniform(0, 1) < 0.85 else random.choice(applicable_positions)


def PGREEDY(agent):
    # Check if pickup and dropoff are applicable
    nextPosition = isDropoffApplicable(agent.position, agent.carrying_block) + \
                   isPickupApplicable(agent.position, agent.carrying_block)

    if nextPosition:
        return random.choice(nextPosition)
    # If not, choose the applicable operator with highest q-value
    applicable_positions = [position for position in checkMoves(agent.position) if not checkCollision(position)]
    # max_q_value = max([q_matrix[state][action] for action in applicable_actions])

    # best_actions = [action for action in applicable_actions if q_matrix[state][action] == max_q_value]
    # # If there is only one best action, choose it with probability 0.85
    best_actions = getBestActions(applicable_positions, agent)
    # If there is only one best action, choose it
    if len(best_actions) == 1:
        return best_actions[0]
    # If there are multiple best actions, choose one of them randomly
    else:
        return random.choice(best_actions)


def makeAgent(name, position, algo):  # so we can easily change algos?
    new_agent = Agent()
    new_agent.position = position
    new_agent.algo = algo
    new_agent.actions = actions.keys()
    new_agent.q_table = np.zeros((length * height * depth, len(new_agent.actions)))
    # if we ever need to change the movements??
    agents.update({name: new_agent})


def getMove(old_position, new_position):
    east_west = new_position[0] - old_position[0]
    north_south = new_position[1] - old_position[1]
    up_down = new_position[2] - old_position[2]
    return east_west, north_south, up_down


def updateQTable(agent, old_position, reward):
    action = getMove(old_position, agent.position)
    position_index = list(cube.keys()).index(agent.position)
    old_position_index = list(cube.keys()).index(old_position)
    action_index = list(agent.actions).index(action)

    agent.q_table[old_position_index][action_index] = agent.q_table[old_position_index][action_index] + alpha * \
                                                      (reward + gamma * max(agent.q_table[position_index]) -
                                                       agent.q_table[old_position_index][action_index])


def checkTerminalState():
    num_dropoffs_full = 0
    for cell in dropoffs:
        if cube[cell].holding == cube[cell].max_capacity:
            num_dropoffs_full += 1

    return True if num_dropoffs_full == len(dropoffs) else False
