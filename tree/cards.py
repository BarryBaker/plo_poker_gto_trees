import numpy as np
from itertools import combinations


from .static import card_values, suit_values
from icecream import ic as qw


class Cards:
    def __init__(self, cards) -> None:
        if type(cards) is str:
            self.cards = [
                (card_values[cards[i]], suit_values[cards[i + 1]])
                for i in range(0, len(cards), 2)
            ]
        if type(cards) is list:
            self.cards = cards

    @property
    def ranks(self):
        return np.array([i[0] for i in self.cards])

    @property
    def suits(self):
        return np.array([i[1] for i in self.cards])

    @property
    def uranks(self):
        return np.unique(self.ranks, return_counts=True)

    @property
    def usuits(self):
        return np.unique(self.suits, return_counts=True)


class Board(Cards):
    # def __init__(self):
    #     super().__init__()

    @property
    def cards_turn(self):
        return self.cards[:4]

    @property
    def usuits_turn(self):
        return np.unique(
            np.array([i[1] for i in self.cards_turn]), return_counts=True
        )

    @property
    def paired_map(self):
        unique, count = self.uranks
        return count

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
        ranks = self.uranks[0]

        str8s = self.str8
        str8_cards = [(i[0], i[1]) for i in str8s]

        str_draws = []
        for next in range(2, 15):
            if next not in ranks:
                next_board = Board(self.cards + [(next, 0)])
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

        return str_draws

    @property
    def sdbl(self):
        str8 = [(i[0], i[1]) for i in self.str8 if i[2] == 0]
        str8 = [i for j in str8 for i in j]
        sd = np.array([(i[0], i[1]) for i in self.str8_draw if i[2] == 0])

        sd, count = np.unique(sd, return_counts=True, axis=0)
        return list(set([i for i in sd[count == 2].flatten()] + str8))

    def __repr__(self):
        return f"|| {' '.join(list(card_values.keys())[list(card_values.values()).index(i[0])]+list(suit_values.keys())[list(suit_values.values()).index(i[1])] for i in self.cards)} ||"
