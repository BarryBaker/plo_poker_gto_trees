import numpy as np
import pickle
import glob
import os

from time import time
from icecream import ic as qw
from tqdm import tqdm

from tree.static import actions_order, card_values_inv
from tree.cards import Cards, Board
from tree.omaha.made import fn as made
from tree.omaha.str8 import fn as str8
from tree.omaha.flush import fn as flush
from tree.omaha.ranks import exact_cards


def load_strat(gto_path, board, situation, line):
    situation["poss"] = "_".join(situation["poss"])

    file = glob.glob(
        os.path.join(gto_path, f"{'_'.join(list(situation.values()))}.obj")
    )[0]

    with open(file, "rb") as f:
        a = pickle.load(f)[line]

    actions = sorted(list(a.columns), key=actions_order)
    cards = Cards(a)
    board = Board(board)
    qw(board)

    start = time()

    for f in flush:
        a[flush[f].__name__] = flush[f](cards, board)
    for f in made:
        a[made[f].__name__] = made[f](cards, board)

    str8s = board.str8
    str8_draws = board.str8_draw
    str8_sdbl = board.sdbl

    a["str8"] = str8["str8"](cards, str8s)
    a["str8_1"] = str8["str8"](cards, str8s)
    a["sdbl"] = str8["sdbl"](cards, str8_sdbl)
    a["dsdbl"] = str8["dsdbl"](cards, str8_sdbl)

    if len(str8_draws) > 0:
        # start2 = time()
        # sd = str8["sd"](cards, str8_draws)
        # qw(time() - start2)

        a["wrap_1"] = str8["sd"](cards, str8_draws, 0)
        a["wrap"] = str8["sd"](cards, str8_draws, 1)
        a["oesd_1"] = str8["sd"](cards, str8_draws, 2)
        a["oesd"] = str8["sd"](cards, str8_draws, 3)
        a["gs_1"] = str8["sd"](cards, str8_draws, 4)
        a["gs"] = str8["sd"](cards, str8_draws, 5)

    # for i in range(2, 15):
    #     a[str(card_values_inv[i])] = exact_cards(cards, i)
    #     a[str(card_values_inv[i]) + str(card_values_inv[i])] = exact_cards(
    #         cards, i, 2
    #     )

    a.drop(
        [
            c
            for c in [i for i in a.columns if i not in actions]
            if (np.all(a[c]) or np.all(~a[c]))
        ],
        axis=1,
        inplace=True,
    )
    qw(time() - start)
    qw((a.sample(20)))
    return a, actions
