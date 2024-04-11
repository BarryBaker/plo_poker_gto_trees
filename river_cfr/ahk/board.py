if __name__ == "__main__":
    from static import cardValues
else:
    from .static import cardValues

import numpy as np


class RiverBoard:
    def __init__(self, board: list) -> None:
        self.board = board

    @property
    def ranks(self):
        return np.array([cardValues[i[0]] for i in self.board])

    @property
    def suits(self):
        return np.array([i[1] for i in self.board])

    @property
    def flush(self):
        suits, counts = np.unique(self.suits, return_counts=True)
        if np.max(counts) >= 3:
            return [suits[np.argmax(counts)]]
        return []

    @property
    def paired(self):
        _, counts = np.unique(self.ranks, return_counts=True)
        if np.max(counts) > 1:
            return True
        return False

    @property
    def str8(self):
        ranks, counts = np.unique(self.ranks, return_counts=True)
        if len(ranks) <= 2:
            return False
        return any(
            np.max(ranks[i : i + 3]) - np.min(ranks[i : i + 3]) <= 4
            for i in range(len(ranks) - 2)
        )

    @property
    def flush_draw(self):
        suits, counts = np.unique(self.suits[:4], return_counts=True)
        if np.max(counts) == 2:
            return (
                suits[np.argwhere(counts == np.max(counts))]
                .flatten()
                .tolist()
            )
            # result = [i for i in result if i != self.flush]
            # return result
        return []

    def __repr__(self):
        return f"|| {' '.join([i for i in self.board])} ||"


if __name__ == "__main__":
    from icecream import ic as ip

    ip(RiverBoard(["6c", "8c", "Jh", "Js", "8d"]).str8)
