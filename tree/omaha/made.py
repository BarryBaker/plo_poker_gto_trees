# from tree.cards import Cards
import numpy as np
from icecream import ic as qw
from itertools import combinations


def trips(hole, board):
    unique, count = hole.uranks
    pairs = unique[count >= 2]
    return any(i in board.ranks for i in pairs)


def twop(hole, board):
    unique, count = hole.uranks
    singles = unique[count == 1]

    if np.max(board.paired_map) >= 2:
        return False
    if len(singles) < 2:
        return False

    return any(
        [
            all([j in board.ranks for j in i])
            for i in combinations(singles, 2)
        ]
    )


def tp(hole, board):
    unique, count = board.uranks
    tp = np.max(unique[count == 1])

    return tp in hole.ranks
