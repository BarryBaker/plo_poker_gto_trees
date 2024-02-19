import numpy as np
import pickle
import glob
import os

from time import time
from icecream import ic as qw
from tqdm import tqdm

from omaha._static import actions_order, card_values_inv
from omaha._cards import Cards, Board

from omaha.made import fn as made
from omaha.str8 import fn as str8
from omaha.flush import fn as flush

# from omaha.ranks import exact_cards

gto_path = "/Users/barrybaker/Documents/fromAHK/objs3/"


def get_board_from_link(link: str):
    return link.replace(gto_path, "").split("_")[-1].replace(".obj", "")


def get_pot_from_link(link: str):
    return link.replace(gto_path, "").split("_")[-2]


def get_boards(filters):
    files = [
        glob.glob(f"{gto_path}100_{poss}_{pot}*.obj")
        for poss in filters["poss"]
        for pot in filters["pot"]
    ]

    # files = [glob.glob(f"{gto_path}50*_{'SRP'}*.obj")]
    # def board_filter(b: Board): # FLUSH
    #     return (
    #         len(b.flush) > 0
    #         and len(Board(b.string_cards[:6]).flush) == 0
    #         and len(b.cards == 4)
    #     )

    # def board_filter(b: Board):
    #     return not b.is_flush and not b.is_str8 and not b.is_paired and not b.is_suited and len(b.cards == 4)

    def board_filter(b: Board):
        return (
            not b.is_flush
            and not b.is_str8
            and not b.is_paired
            and not b.is_suited
            and len(b.cards) == 3
        )

    # print(files))
    # for i in files:
    #     for j in i:
    #         # print(type(i), i)
    #         print(j, len(Board(get_board_from_link(j)).cards))
    boards = [
        j
        for i in files
        for j in i
        if len(Board(get_board_from_link(j)).cards) == 3
        # if get_board_from_link(j) == "7s7d2d5c"
        # if board_filter(Board(get_board_from_link(j)))
    ]
    # print(len(boards))
    return boards


def load_strat(a, url):  # line):
    # with open(url, "rb") as f:
    #     a = pickle.load(f)

    # if line not in a:
    #     return "NOLINE"
    # a = a[line]

    actions = sorted(list(a.columns), key=actions_order)
    cards = Cards(a)
    board = Board(get_board_from_link(url))

    # start = time()

    for f in flush:
        a[f] = flush[f](cards, board)

    a["Q"] = made["Q"](cards, board)
    a["FULL"] = made["FULL"](cards, board) & ~a["Q"]
    a["FULL1"] = made["FULL1"](cards, board) & ~a["Q"]
    a["TRIPS"] = made["TRIPS"](cards, board) & ~a["Q"]
    a["TRIPS1"] = made["TRIPS1"](cards, board) & ~a["Q"]
    a["TRIPST"] = made["TRIPST"](cards, board) & ~a["Q"]
    a["2P"] = made["2P"](cards, board) & ~a["TRIPS"]
    a["2PT"] = made["2PT"](cards, board)
    a["TP"] = made["TP"](cards, board)
    a["TPTK"] = made["TPTK"](cards, board)
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
        a["WR"] = str8["sd"](cards, str8_draws, 0)
        a["WR1"] = str8["sd"](cards, str8_draws, 1)
        a["OESD"] = str8["sd"](cards, str8_draws, 2) & ~a["WR"] & ~a["WR1"]
        a["OESD1"] = str8["sd"](cards, str8_draws, 3) & ~a["WR"] & ~a["WR1"]
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
        a["SD"] = a["WR"] | a["OESD"] | a["GS"]

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
