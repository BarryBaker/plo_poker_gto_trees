import numpy as np
import pandas as pd
from itertools import combinations


from ._static import (
    card_values,
    suit_values,
    card_values_inv,
    suit_values_inv,
)
from icecream import ic as qw


class Cards:
    def __init__(self, a: pd.DataFrame) -> None:
        self.cards = np.array(
            [
                [
                    [card_values[c[i]], suit_values[c[i + 1]]]
                    for i in range(0, 8, 2)
                ]
                for c in a.index
            ]
        )
        # qw(range_)
        # sorting_indices = np.lexsort(
        #     (
        #         range_[:, 3, 0],
        #         range_[:, 2, 0],
        #         range_[:, 1, 0],
        #         range_[:, 0, 0],
        #     ),
        #     axis=0,
        # )
        # # qw((range_[:, 0, 0], range_[:, 1, 0], range_[:, 2, 0]))
        # self.range_ = range_[sorting_indices[::-1]]

    @property
    def ranks(self):
        return self.cards[:, :, 0]

    @property
    def suits(self):
        return self.cards[:, :, 1]

    @property
    def empty(self):
        return np.full(self.cards.shape[0], False)

    def __repr__(self):
        rows = 6
        if self.cards.shape[0] > 10:
            return "\n".join(
                [
                    f"| {' '.join([card_values_inv[i[0]]+suit_values_inv[i[1]] for i in cards])} |"
                    for cards in np.vstack(
                        [self.cards[:rows], self.cards[-rows:]]
                    )
                ]
            )
        return "\n".join(
            [
                f"| {' '.join([card_values_inv[i[0]]+suit_values_inv[i[1]] for i in cards])} |"
                for cards in self.cards
            ]
        )


class Board:
    def __init__(self, cards) -> None:
        if type(cards) is str:
            self.cards = np.array(
                [
                    [card_values[cards[i]], suit_values[cards[i + 1]]]
                    for i in range(0, len(cards), 2)
                ]
            )

            self.string_cards = cards
        else:
            self.cards = cards

    @property
    def ranks(self):
        return self.cards[:, 0]

    @property
    def suits(self):
        return self.cards[:, 1]

    @property
    def uranks(self):
        return np.unique(self.ranks, return_counts=True)

    @property
    def usuits(self):
        return np.unique(self.suits, return_counts=True)

    @property
    def turn(self):
        return self.cards[:4]

    @property
    def usuits_turn(self):
        return np.unique(self.cards[:4][:, 1], return_counts=True)

    @property
    def uranks_turn(self):
        return np.unique(self.cards[:4][:, 0], return_counts=True)

    @property
    def flush(self):
        unique, count = self.usuits
        return unique[count >= 3]

    @property
    def fd(self):
        unique, count = self.usuits_turn
        if len(self.flush) > 0:
            return np.array([])

        return unique[count == 2]

    @property
    def bdfd(self):
        if len(self.cards) > 3:
            return np.array([])
        unique, count = self.usuits

        return unique[count == 1]

    @property
    def str8(self):
        def str8_wheel(ranks: np.array):
            three_groups = [
                i
                for i in combinations(sorted(ranks), 3)
                if np.max(i) - np.min(i) <= 4
            ]

            if len(three_groups) == 0:
                return []

            str8_cards = []
            for i in three_groups:
                possible = [
                    j
                    for j in range(
                        max(np.min(i) - 2, 1), min(np.max(i) + 3, 15)
                    )
                    if j not in i
                ]

                for n, k in enumerate(possible[:-1]):
                    new5 = np.concatenate(
                        (i, np.array([k, possible[n + 1]]))
                    )

                    if np.max(new5) - np.min(new5) == 4:
                        to_append = [k, possible[n + 1]]
                        to_append = sorted(
                            [m if m != 1 else 14 for m in to_append]
                        )

                        str8_cards.append(
                            tuple(to_append + [np.max(new5)])
                        )

            return str8_cards

        ranks = self.uranks[0]

        no_wheel = str8_wheel(ranks)

        if 14 in ranks:
            ranks = np.array([i if i != 14 else 1 for i in ranks])
        wheel = str8_wheel(ranks)

        str8s = list(set(wheel + no_wheel))

        highs = sorted(list(set([i[2] for i in str8s])), reverse=True)

        str8s = [(i[0], i[1], highs.index(i[2])) for i in str8s]

        str_cards = list(set([(i[0], i[1]) for i in str8s]))
        result = []
        for i in str_cards:
            best_str = min([j[2] for j in str8s if (j[0], j[1]) == i])

            result.append(tuple(list(i) + [best_str]))
        return result

    @property
    def str8_draw(self):
        if len(self.cards) == 5:
            return []

        ranks = self.uranks_turn[0]

        str8s = self.str8
        str8_cards = [(i[0], i[1]) for i in str8s]

        str_draws = []
        for next in range(2, 15):
            if next not in ranks:
                next_board = Board(np.vstack([self.cards, [next, 0]]))

                for ns in next_board.str8:
                    to_append = tuple(list(ns) + [next])

                    if (ns[0], ns[1]) not in str8_cards:
                        str_draws.append(to_append)
                    else:
                        matched = [
                            i
                            for i in str8s
                            if i[0] == ns[0] and i[1] == ns[1]
                        ][0]

                        if ns[2] < matched[2]:
                            str_draws.append(to_append)
        str_draws = sorted(str_draws, key=lambda x: 10 * x[0] + x[1])
        str8_cards = list(set([j for i in str_draws for j in i[:2]]))

        result = {}  # 0:wrap,1wrap1...5:gs1
        for n in [2, 3, 4]:
            for cardc in combinations(str8_cards, n):
                str8s = [
                    i
                    for i in str_draws
                    if any(
                        [
                            j[0] == i[0] and j[1] == i[1]
                            for j in combinations(cardc, 2)
                        ]
                    )
                ]

                makes_the_str8_with = [(i[2], i[3]) for i in str8s]
                all_str8_cards = list(set([i[3] for i in str8s]))
                makes_high_str8_with = [
                    min([j[0] for j in makes_the_str8_with if j[1] == i])
                    for i in all_str8_cards
                ]
                outs = len(makes_high_str8_with)
                if outs > 0:
                    nut = max(makes_high_str8_with) == 0
                    result[cardc] = (outs, nut)
        # qw(result)
        return result

    @property
    def sdbl(self):
        str8 = [(i[0], i[1]) for i in self.str8 if i[2] == 0]
        str8 = [i for j in str8 for i in j]
        sd = np.array(
            [
                (i[0], i[1])
                for i in self.str8_draw
                if self.str8_draw[i][0] == 2
                and self.str8_draw[i][1]
                and len(i) == 2
            ]
        )
        # sd, count = np.unique(sd, return_counts=True, axis=0)

        return list(sd.flatten()) + str8

    @property
    def remaining_ranks(self):
        return [i for i in card_values_inv if i not in self.uranks[0]]

    @property
    def is_flush(self):
        return len(self.flush) > 0

    @property
    def is_str8(self):
        return len(self.str8) > 0

    @property
    def is_paired(self):
        return np.max(self.uranks[1]) > 1

    @property
    def is_suited(self):
        return np.max(self.usuits[1]) > 1

    def __repr__(self):
        return f"| {' '.join([card_values_inv[i[0]]+suit_values_inv[i[1]] for i in self.cards])} |"
