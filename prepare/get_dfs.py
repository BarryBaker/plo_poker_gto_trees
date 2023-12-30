import os
import glob
import pandas as pd
import pickle
from icecream import ic as qw
from tqdm import tqdm


gto_path = "/Users/barrybaker/Documents/easygto/easygto_back/app/GTO/"

files = glob.glob(os.path.join(gto_path, "*.csv"))

csvs = []
for file in tqdm(files):
    f = pd.read_csv(file, index_col="combo")
    # if "ev" in f.columns:
    csvs.append(file.replace(gto_path, ""))

with open("csvs.obj", "wb") as json_file:
    pickle.dump(csvs, json_file)
