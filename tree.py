import pandas as pd
import pickle
import glob
import os
from functools import reduce
from time import time
from icecream import ic as qw
from tqdm import tqdm

from tree.cards import Cards, Board
from tree.omaha.made import trips, tp, twop
from tree.omaha.str8 import str8, sd, sdbl, dsdbl
from tree.omaha.flush import fd

start = time()
gto_path = "/Users/barrybaker/Documents/fromAHK/objs3/"

board = "9s8d7d"
# board = "JsTd2c"

situation = {
    "stack": "100",
    "poss": ["BTN", "BB"],
    "pot": "SRP",
    "board": board,
}
line = "C"
situation["poss"] = "_".join(situation["poss"])

# files = glob.glob(
#     os.path.join(gto_path, f"{'_'.join(list(situation.values()))}_*")
# )
file = glob.glob(
    os.path.join(gto_path, f"{'_'.join(list(situation.values()))}.obj")
)[0]

with open(file, "rb") as f:
    a = pickle.load(f)[line]

actions = list(a.columns)


a["hole"] = a.apply(lambda x: Cards(x.name), axis=1)
board = Board(board)

str8s = board.str8
str8_draws = board.str8_draw
str8_sdbl = board.sdbl


def add_col(fn):
    a[fn.__name__] = a.apply(lambda x: fn(x.hole, board), axis=1)


def add_col_str8(fn):
    a[fn.__name__] = a.apply(lambda x: fn(x.hole, str8s), axis=1)


def add_col_str8_draws(fn):
    a[fn.__name__] = a.apply(lambda x: fn(x.hole, str8_draws), axis=1)


def add_col_sdbl(fn):
    a[fn.__name__] = a.apply(lambda x: fn(x.hole, str8_sdbl), axis=1)


add_col(trips)
add_col(tp)
add_col(twop)
add_col(fd)
add_col_str8(str8)
add_col_str8_draws(sd)
add_col_sdbl(sdbl)
add_col_sdbl(dsdbl)

a["wrap"] = a.sd.apply(lambda x: x[0] > 2)
a["wrap1"] = a.sd.apply(lambda x: x[0] > 2 and x[1])
a["oesd"] = a.sd.apply(lambda x: x[0] == 2)
a["oesd1"] = a.sd.apply(lambda x: x[0] == 2 and x[1])
a["gs"] = a.sd.apply(lambda x: x[0] == 1)
a["gs1"] = a.sd.apply(lambda x: x[0] == 1 and x[1])

a.drop(["hole", "sd"], axis=1, inplace=True)
qw(board, a.sample(20))

with open("a.obj", "wb") as f:
    pickle.dump(a, f)
