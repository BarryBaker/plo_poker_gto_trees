from tree.cards import Hole
import numpy as np


def test_hole():
    hole = Hole("Ac9h7h6h")
    np.testing.assert_array_equal(hole.ranks, [14, 9, 7, 6])
