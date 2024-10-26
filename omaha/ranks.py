# from tree.cards import Cards
import numpy as np

from itertools import combinations

from ._cards import Board, Cards
from ._utils import f1, f2, f1_card
from ._static import card_values_inv


def exact_cards(cards: Cards, card, nr=1):
    ranks = cards.ranks
    if nr == 1:
        return f1(ranks, card)
    return f2(ranks, card)
