import numpy as np
from icecream import ic as qw

from tree.cards import Cards, Board
from tree.omaha.made import trips, tp, twop
from tree.omaha.flush import fd
from tree.omaha.str8 import str8, sd


h = Cards("AsKd4s5h")
b = Board("KhQc9s")
# qw(b.fd)
qw(fd(h, b))
