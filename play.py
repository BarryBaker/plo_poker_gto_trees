import numpy as np
import pandas as pd
import pickle
import glob
import os
from icecream import ic as qw
import json

# import ast

file = "/Users/barrybaker/Documents/blackcard2/blackcard2_back/app/saved/100_CO_BTN_3BP_AsJsTd_.obj"
trees = "/Users/barrybaker/Documents/blackcard2/blackcard2/src/assets/trees.json"

with open(file, "rb") as f:
    a = pickle.load(f)

with open(trees) as user_file:
    a = json.load(user_file)

qw(a[:10])
# qw([1, 2, 3, 4, 5, 6, 7][::2])
bb = 5

print(list("[1,2]"))

# def aaa():
#     bb = 6


# aaa()
# print(bb)
