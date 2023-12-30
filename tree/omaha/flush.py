# from tree.cards import Cards
import numpy as np
from icecream import ic as qw
from itertools import combinations

from ..cards import Board, Cards
from ..static import card_values, suit_values


def fd(hole: Cards, board: Board):
    fd = board.fd
    if len(fd) == 0:
        return False

    fd_ranks = [i[0] for i in board.cards if i[1] == fd[0]]
    rest_ranks = [i for i in card_values.values() if i not in fd_ranks]

    suits, count = hole.usuits

    if fd[0] not in suits:
        return False

    return count[suits == fd[0]][0] >= 2
