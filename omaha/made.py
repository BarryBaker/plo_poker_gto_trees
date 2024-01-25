# from tree.cards import Cards
import numpy as np
from icecream import ic as qw
from itertools import combinations

from ._cards import Board, Cards
from ._utils import f1, f2, f1_card
from ._static import card_values_inv


def quads(cards: Cards, board: Board):
    ranks = cards.ranks
    unique, counts = board.uranks

    if np.max(counts) < 2:
        return cards.empty

    if np.max(counts) == 2:
        doubles = unique[counts == 2]
        return np.any(
            [f2(ranks, card) for card in doubles],
            axis=0,
        )
    triple = unique[counts > 2][0]
    return f1(ranks, triple)


def full(cards: Cards, board: Board):
    ranks = cards.ranks
    unique, counts = board.uranks

    if np.max(counts) < 2:
        return cards.empty

    singles = unique[counts == 1]
    doubles = unique[counts == 2]

    if np.max(counts) == 2:
        if len(doubles) > 1:
            return np.any(
                [
                    np.all([f1(ranks, i) for i in ranks2], axis=0)
                    for ranks2 in combinations(unique, 2)
                ],
                axis=0,
            )

        return np.any(
            [
                np.any([f2(ranks, i) for i in singles], axis=0),
                np.all(
                    [
                        np.any([f1(ranks, i) for i in singles], axis=0),
                        np.any([f1(ranks, i) for i in doubles], axis=0),
                    ],
                    axis=0,
                ),
            ],
            axis=0,
        )

    triple = unique[counts > 2][0]
    higher_ranks = unique[unique > triple]

    return np.any(
        [f2(ranks, card) for card in higher_ranks],
        axis=0,
    )


def full_1(cards: Cards, board: Board):
    ranks = cards.ranks
    unique, counts = board.uranks

    if np.max(counts) < 2:
        return cards.empty

    singles = unique[counts == 1]
    doubles = unique[counts == 2]

    if np.max(counts) == 2:
        if counts[-1] == 1:
            return f2(ranks, unique[-1])

        if (
            np.array_equal(counts, np.array([1, 2]))
            or np.array_equal(counts, np.array([1, 1, 2]))
            or np.array_equal(counts, np.array([1, 1, 1, 2]))
            or np.array_equal(counts, np.array([2, 1, 2]))
        ):
            return np.all(
                [f1(ranks, doubles[-1]), f1(ranks, singles[-1])], axis=0
            )

        if np.array_equal(counts, np.array([2, 2])) or np.array_equal(
            counts, np.array([1, 2, 2])
        ):
            return np.all(
                [f1(ranks, doubles[-1]), f1(ranks, doubles[-2])], axis=0
            )

    triple = unique[counts > 2][0]
    higher_ranks = unique[unique > triple]
    if len(higher_ranks) > 0:
        return f2(ranks, higher_ranks[-1])

    return cards.empty


def trips(cards: Cards, board: Board):
    ranks = cards.ranks
    unique, counts = board.uranks

    if np.max(counts) >= 3:
        return cards.empty

    if np.max(counts) >= 2:
        doubles = unique[counts == 2]
        return np.any(
            [f1(ranks, card) for card in doubles],
            axis=0,
        )

    return np.any(
        [f2(ranks, card) for card in unique],
        axis=0,
    )


def trips_1(cards: Cards, board: Board):
    ranks = cards.ranks
    unique, counts = board.uranks

    if np.max(counts) >= 3:
        return cards.empty

    if np.max(counts) >= 2:
        doubles = unique[counts == 2]
        return np.all(
            [f1(ranks, doubles[-1]), f1(ranks, board.remaining_ranks[0])],
            axis=0,
        )

    return f2(ranks, unique[-1])


def trips_top(cards: Cards, board: Board):
    ranks = cards.ranks
    unique, counts = board.uranks

    if np.max(counts) != 2:
        return cards.empty

    doubles = unique[counts == 2]
    if len(doubles) == 1:
        return cards.empty

    return f1(ranks, unique[-1])


def twop(cards: Cards, board: Board):
    ranks = cards.ranks
    board_ranks = board.ranks

    if np.max(board.uranks[1]) > 1:
        return cards.empty

    return np.any(
        [
            np.all([f1(ranks, i) for i in ranks2], axis=0)
            for ranks2 in combinations(board_ranks, 2)
        ],
        axis=0,
    )


def twop_1(cards: Cards, board: Board):
    ranks = cards.ranks
    unique, counts = board.uranks

    if np.max(counts) > 1:
        return cards.empty

    return np.all([f1(ranks, i) for i in unique[-2:]], axis=0)


def op(cards: Cards, board: Board):
    ranks = cards.ranks

    unique, counts = board.uranks
    overs = [i for i in card_values_inv if i > np.max(unique)]

    if len(overs) == 0:
        return cards.empty

    return np.any(
        [f2(ranks, card) for card in overs],
        axis=0,
    )


def rr(cards: Cards, board: Board):
    ranks = cards.ranks

    unique, counts = board.uranks
    remaining = [
        i
        for i in card_values_inv
        if i < np.max(unique) and i not in unique
    ]

    return np.any(
        [f2(ranks, card) for card in remaining],
        axis=0,
    )


def lrr(cards: Cards, board: Board):
    ranks = cards.ranks

    unique, counts = board.uranks
    remaining = [
        i
        for i in card_values_inv
        if i < np.max(unique) and i not in unique
    ]
    remaining = remaining[int(len(remaining) / 2) :]
    return np.any(
        [f2(ranks, card) for card in remaining],
        axis=0,
    )


def hrr(cards: Cards, board: Board):
    ranks = cards.ranks

    unique, counts = board.uranks
    remaining = [
        i
        for i in card_values_inv
        if i < np.max(unique) and i not in unique
    ]
    remaining = remaining[: int(len(remaining) / 2)]
    return np.any(
        [f2(ranks, card) for card in remaining],
        axis=0,
    )


def tp(cards: Cards, board: Board):
    ranks = cards.ranks

    unique, counts = board.uranks
    singles = unique[counts == 1]

    if len(singles) == 0:
        return cards.empty

    tp = singles[-1]

    return f1(ranks, tp)


def tp_1(cards: Cards, board: Board):
    ranks = cards.ranks
    unique, counts = board.uranks
    singles = unique[counts == 1]

    if len(singles) == 0:
        return cards.empty

    if np.max(counts) > 2:
        return cards.empty

    tp = singles[-1]
    tk = board.remaining_ranks[0]

    if np.max(counts) == 1:
        return np.all(
            [f1(ranks, tp), f1(ranks, tk)],
            axis=0,
        )

    doubles = unique[counts == 2]
    over_doubles = singles[singles > doubles[-1]]
    if len(over_doubles) >= 2:
        return np.all(
            [f1(ranks, over_doubles[-1]), f1(ranks, over_doubles[-2])],
            axis=0,
        )

    return np.all(
        [f1(ranks, tp), f1(ranks, tk)],
        axis=0,
    )


def mp(cards: Cards, board: Board):
    ranks = cards.ranks

    unique, counts = board.uranks

    singles = unique[counts == 1]

    if len(singles) < 3:
        return cards.empty

    if len(singles) < 5:
        mp = singles[1:-1]
    else:
        mp = singles[2:-1]

    return np.any(
        [f1(ranks, card) for card in mp],
        axis=0,
    )


def lp(cards: Cards, board: Board):
    ranks = cards.ranks
    unique, counts = board.uranks
    singles = unique[counts == 1]

    if len(singles) < 2:
        return cards.empty

    if len(singles) < 5:
        lp = singles[0:1]
    else:
        lp = singles[0:2]

    return np.any(
        [f1(ranks, card) for card in lp],
        axis=0,
    )


def bop(cards: Cards, board: Board):
    ranks = cards.ranks
    unique, counts = board.uranks
    singles = unique[counts == 1]

    if len(singles) < 2:
        return cards.empty

    return np.any(
        [f1(ranks, card) for card in singles],
        axis=0,
    )


fn = {
    "Q": quads,
    "FULL": full,
    "FULL1": full_1,
    "TRIPS": trips,
    "TRIPS1": trips_1,
    "TRIPST": trips_top,
    "2P": twop,
    "2PT": twop_1,
    "TP": tp,
    "TP1": tp_1,
    "MP": mp,
    "LP": lp,
    "BOP": bop,
    "OP": op,
    "RR": rr,
    "LRR": lrr,
    "HRR": hrr,
}
# fn = {f.__name__: f for f in fn}
