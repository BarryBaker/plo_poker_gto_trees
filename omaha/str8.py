# from tree.cards import Cards
import numpy as np
import pandas as pd
from icecream import ic as qw
from itertools import combinations

# from ._static import card_values
from ._cards import Cards, Board
from ._utils import f1, f2, f1_card


def str8(cards: Cards, str8s: list):
    ranks = cards.ranks
    str8_cards = [(i[0], i[1]) for i in str8s]

    return np.any(
        [
            np.all(
                [f1(ranks, card) for card in card2],
                axis=0,
            )
            for card2 in str8_cards
        ],
        axis=0,
    )


def str8_1(cards: Cards, str8s: list):
    ranks = cards.ranks
    str8_cards = [(i[0], i[1]) for i in str8s if i[2] == 0]

    return np.any(
        [
            np.all(
                [f1(ranks, card) for card in card2],
                axis=0,
            )
            for card2 in str8_cards
        ],
        axis=0,
    )


def sd(cards: Cards, str8_draws: list, str8_code):
    ranks = cards.ranks
    if str8_code == 0:
        str8_draws = [i for i in str8_draws if str8_draws[i][0] > 2]
    if str8_code == 1:
        str8_draws = [
            i
            for i in str8_draws
            if str8_draws[i][0] > 2 and str8_draws[i][1]
        ]
    if str8_code == 2:
        str8_draws = [i for i in str8_draws if str8_draws[i][0] == 2]
    if str8_code == 3:
        str8_draws = [
            i
            for i in str8_draws
            if str8_draws[i][0] == 2 and str8_draws[i][1]
        ]
    if str8_code == 4:
        str8_draws = [i for i in str8_draws if str8_draws[i][0] == 1]
    if str8_code == 5:
        str8_draws = [
            i
            for i in str8_draws
            if str8_draws[i][0] == 1 and str8_draws[i][1]
        ]

    return np.any(
        [
            np.all([f1(ranks, card) for card in cardc], axis=0)
            for cardc in str8_draws
        ],
        axis=0,
    )
    # if len(str8_draws) == 0:
    #     return None

    # def outs(cards4):
    #     unique = np.unique(cards4)

    #     hole_str8_draws = [
    #         j
    #         for j in str8_draws
    #         for i in combinations(unique, 2)
    #         if j[0] == i[0] and j[1] == i[1]
    #     ]

    #     if len(hole_str8_draws) == 0:
    #         return -1

    #     str_completing_cards = list(set([i[3] for i in hole_str8_draws]))
    #     nut = (
    #         max(
    #             [
    #                 min([j[2] for j in hole_str8_draws if j[3] == i])
    #                 for i in str_completing_cards
    #             ]
    #         )
    #         == 0
    #     )
    #     outs = len(str_completing_cards)

    #     if outs > 2 and not nut:
    #         return 0
    #     if outs > 2 and nut:
    #         return 1
    #     if outs == 2 and not nut:
    #         return 2
    #     if outs == 2 and nut:
    #         return 3
    #     if outs == 1 and not nut:
    #         return 4
    #     if outs == 1 and nut:
    #         return 5

    # return np.apply_along_axis(outs, 1, ranks)


def sdbl(cards: Cards, sdbl: list):
    ranks = cards.ranks
    return np.any([f1(ranks, i) for i in sdbl], axis=0)


def dsdbl(cards: Cards, sdbl: list):
    ranks = cards.ranks
    return np.any([f2(ranks, i) for i in sdbl], axis=0)


fn = [str8, str8_1, sd, sdbl, dsdbl]
fn = {f.__name__: f for f in fn}
