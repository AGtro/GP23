from enum import Enum, auto

cube = {}
action_cost = -1


class CellType(Enum):
    normalCell = auto()
    riskyCell = auto()
    pickupCell = auto()
    dropoffCell = auto()


class Cell:
    cellType = CellType.normalCell
    position = (0, 0, 0)
    reward = 0
    capacity = 0
    utility = 0


def addCell(position, ctype=CellType.normalCell, reward=0, capacity=0, utility=0):
    if position not in cube:
        cell = Cell()
        cell.cellType = ctype
        cell.position = position
        cell.reward = reward
        cell.capacity = capacity
        cell.utility = utility
        cube.update({position: cell})


for i in [(2, 2, 1), (3, 3, 2)]:
    addCell(i, CellType.pickupCell, 14, 10)

for i in [(1, 1, 1), (1, 1, 3), (3, 1, 1), (3, 2, 3)]:
    addCell(i, CellType.dropoffCell, 14, 5)

for i in [(2, 2, 2), (3, 2, 1)]:
    addCell(i, CellType.riskyCell, 2*action_cost)


class Agent:
    position = (0, 0, 0)
    q_table = [0]*27
    carrying_block = False


def checkMoves(position):
    moves = []
    x, y, z = position
    offsets = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    for dx, dy, dz in offsets:
        if 0 <= x + dx < 4 and 0 <= y + dy < 4 and 0 <= z + dz < 4:
            moves.append((x + dx, y + dy, z + dz))

    return moves


def pickup(carry, reward, position):
    if not carry:
        return True, reward + cube[position].reward
    return carry, reward + action_cost


def dropoff(carry, reward, position):
    if carry:
        return False, reward + cube[position].reward
    return carry, reward + action_cost
