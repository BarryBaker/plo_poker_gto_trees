import numpy as np


def f1_card(array, toFind: tuple):
    return np.any(
        np.any(array == toFind[0], axis=2)
        & np.any(array == toFind[1], axis=2),
        axis=1,
    )


def f1(array, toFind):
    return np.any(array == toFind, axis=1)


def f2(array, toFind):
    return np.count_nonzero(array == toFind, axis=1) >= 2
