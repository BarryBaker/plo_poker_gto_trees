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

gto_path = "/Users/barrybaker/Documents/fromAHK/objs3/"


def get_boards(situation=""):
    if situation == "":
        files = glob.glob(f"{gto_path}*.obj")
    else:
        files = glob.glob(
            os.path.join(
                gto_path, f"{'_'.join(list(situation.values()))}*.obj"
            )
        )

    boards = [
        Board(
            f.replace("_".join(list(situation.values())), "")
            .replace(".obj", "")
            .replace(gto_path, "")
            .replace("_", "")
        )
        for f in files
    ]

    return [f for f in boards if len(f.cards) == 4]


def load_strat(situation, board: Board, line):
    file = glob.glob(
        os.path.join(
            gto_path,
            f"{'_'.join(list(situation.values()))}_{board.string_cards}.obj",
        )
    )[0]
    # qw(file)
    with open(file, "rb") as f:
        a = pickle.load(f)
    if line not in a:
        return "NOLINE"
    a = a[line]
    # qw(a)
    actions = sorted(list(a.columns), key=actions_order)
    cards = Cards(a)
    # board = Board(board)
    # qw(board)

    # start = time()

    for f in flush:
        a[f] = flush[f](cards, board)

    # for f in made:
    #     a[f] = made[f](cards, board)

    a["Q"] = made["Q"](cards, board)
    a["FULL"] = made["FULL"](cards, board) & ~a["Q"]
    a["FULL1"] = made["FULL1"](cards, board) & ~a["Q"]
    a["TRIPS"] = made["TRIPS"](cards, board) & ~a["Q"]
    a["TRIPS1"] = made["TRIPS1"](cards, board) & ~a["Q"]
    a["TRIPST"] = made["TRIPST"](cards, board) & ~a["Q"]
    a["2P"] = made["2P"](cards, board) & ~a["TRIPS"]
    a["2PT"] = made["2PT"](cards, board)
    a["TP"] = made["TP"](cards, board)
    a["MP"] = made["MP"](cards, board)
    a["LP"] = made["LP"](cards, board)
    a["BOP"] = made["BOP"](cards, board)
    a["OP"] = made["OP"](cards, board)
    a["RR"] = made["RR"](cards, board)
    a["LRR"] = made["LRR"](cards, board)
    a["HRR"] = made["HRR"](cards, board)

    str8s = board.str8
    str8_draws = board.str8_draw
    str8_sdbl = board.sdbl

    a["STR"] = str8["str8"](cards, str8s)
    a["STR1"] = str8["str8"](cards, str8s)
    a["SDBL"] = str8["sdbl"](cards, str8_sdbl)
    a["DSDBL"] = str8["dsdbl"](cards, str8_sdbl)

    if len(str8_draws) > 0:
        # start2 = time()
        # sd = str8["sd"](cards, str8_draws)
        # qw(time() - start2)

        a["WR"] = str8["sd"](cards, str8_draws, 0)
        a["WR1"] = str8["sd"](cards, str8_draws, 1)
        a["OESD"] = str8["sd"](cards, str8_draws, 2) & ~a["WR"] & ~a["WR1"]
        a["OESD1"] = (
            str8["sd"](cards, str8_draws, 3) & ~a["WR"] & ~a["WR1"]
        )
        a["GS"] = (
            str8["sd"](cards, str8_draws, 4)
            & ~a["WR"]
            & ~a["WR1"]
            & ~a["OESD"]
            & ~a["OESD1"]
        )
        a["GS1"] = (
            str8["sd"](cards, str8_draws, 5)
            & ~a["WR"]
            & ~a["WR1"]
            & ~a["OESD"]
            & ~a["OESD1"]
        )

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
    # qw(time() - start)

    return a, actions
