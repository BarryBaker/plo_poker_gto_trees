import numpy as np
import pandas as pd
import pickle
import glob
import os
from icecream import ic as qw


file = "/Users/barrybaker/Documents/blackcard2/blackcard2_back/app/saved/100_CO_BTN_3BP_AsJsTd_.obj"


with open(file, "rb") as f:
    a = pickle.load(f)

qw(a)
# qw([1, 2, 3, 4, 5, 6, 7][::2])
