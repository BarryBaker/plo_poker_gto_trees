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
            i for i in str8_draws if str8_draws[i][0] > 2 and str8_draws[i][1]
        ]
    if str8_code == 2:
        str8_draws = [i for i in str8_draws if str8_draws[i][0] == 2]
    if str8_code == 3:
        str8_draws = [
            i for i in str8_draws if str8_draws[i][0] == 2 and str8_draws[i][1]
        ]
    if str8_code == 4:
        str8_draws = [i for i in str8_draws if str8_draws[i][0] == 1]
    if str8_code == 5:
        str8_draws = [
            i for i in str8_draws if str8_draws[i][0] == 1 and str8_draws[i][1]
        ]

    return np.any(
        [np.all([f1(ranks, card) for card in cardc], axis=0) for cardc in str8_draws],
        axis=0,
    )


def sdbl(cards: Cards, sdbl: list):
    ranks = cards.ranks
    return np.any([f1(ranks, i) for i in sdbl], axis=0)


def dsdbl(cards: Cards, sdbl: list):
    ranks = cards.ranks
    return np.any([f2(ranks, i) for i in sdbl], axis=0)


fn = [str8, str8_1, sd, sdbl, dsdbl]
fn = {f.__name__: f for f in fn}
