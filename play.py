import numpy as np
import pandas as pd
import pickle
import glob
import os
from icecream import ic as qw


file = "/Users/barrybaker/Documents/blackcard2/blackcard2_back/app/saved/100_MP_BB_SRP_Th5h5d_C.obj"


with open(file, "rb") as f:
    a = pickle.load(f)

qw(a)
