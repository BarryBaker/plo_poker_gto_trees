import numpy as np
import pandas as pd
from icecream import ic as qw

from omaha._cards import Cards, Board
from omaha.flush import fn
from omaha.flush import fd
from omaha.str8 import str8, sd


h = Cards(
    pd.DataFrame(
        index=[
            "9s9d5s5h",
            "KsKd5s5c",
            "AsAd6s6c",
        ]
    )
)

b = Board("Qh9c5s8sKd")
# # qw(b.fd)
qw(fn["FBL"](h, b))
