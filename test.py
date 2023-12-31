import numpy as np
import pandas as pd

from icecream import ic as qw
import pickle
import glob
import os

from tree.omaha.utils import f1, f2, f1_card
from tree.static import actions_order, card_values, suit_values
from tree.cards import Cards, Board

from tree.omaha.made import fn as made
from tree.omaha.str8 import fn as str8
from tree.omaha.flush import fn as flush

r = Cards(
    pd.DataFrame(
        index=[
            "AcTc9d6h",
            "KsKcJh2c",
            "Ts9h9c2c",
            "Kh6c5h4s",
        ]
    )
)
# qw(r)
b = Board("KhTc4c")

# str8s = b.str8
str8_draws = b.str8_draw
str8_sdbl = b.sdbl
# qw(f1_card(r.range_, (14, 3)))
qw(str8_sdbl)
qw(r, "", b)
qw(flush["fd"](r, b))
# qw(outs, nut)
# qw("wrap", outs > 2)
# qw("wrap1", (outs > 2) & nut)
# qw("oesd", outs == 2)
# qw("oesd1", (outs == 2) & nut)
# qw("gs", outs == 1)
# qw("gs1", (outs == 1) & nut)
