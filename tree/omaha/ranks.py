# from tree.cards import Cards
import numpy as np
from icecream import ic as qw
from itertools import combinations

from ..cards import Board, Cards
from .utils import f1, f2, f1_card
from ..static import card_values_inv


def exact_cards(cards: Cards, card, nr=1):
    ranks = cards.ranks
    if nr == 1:
        return f1(ranks, card)
    return f2(ranks, card)
