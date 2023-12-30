# from tree.cards import Cards
import numpy as np
from icecream import ic as qw
from itertools import combinations

from ..static import card_values
from ..cards import Board, Cards


def str8(hole: Cards, str8s: list):
    unique, count = hole.uranks
    str8_cards = [(i[0], i[1]) for i in str8s]
    return any([i in str8_cards for i in combinations(unique, 2)])


def sd(hole: Cards, str8_draws: list):
    unique, count = hole.uranks
    if len(str8_draws) == 0:
        return 0, False
    hole_str8_draws = [
        j
        for j in str8_draws
        for i in combinations(unique, 2)
        if j[0] == i[0] and j[1] == i[1]
    ]
    if len(hole_str8_draws) == 0:
        return 0, False

    str_completing_cards = list(set([i[3] for i in hole_str8_draws]))
    nutiness = max([i[2] for i in hole_str8_draws]) == 0

    return len(str_completing_cards), nutiness


def sdbl(hole: Cards, sdbl: list):
    unique, count = hole.uranks

    return any([i in sdbl for i in unique])


def dsdbl(hole: Cards, sdbl: list):
    unique, count = hole.uranks
    pairs = unique[count >= 2]
    return any([i in sdbl for i in pairs])
