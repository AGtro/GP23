

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


def pickup(carry, reward):
    if not carry:
        return True, reward + 14
    return carry, reward - 1


def dropOff(carry, reward):
    if carry:
        return False, reward + 14
    return carry, reward - 1

