import glob
import os
from icecream import ic as qw
import shutil
import pickle


path = "/Users/barrybaker/Documents/fromAHK/objs3/"
a = glob.glob(
    f"{path}*.obj",
)
# a = [i.replace(path, "").replace(".obj", "") for i in a]
# a = [i for i in a if len(i.split("_")[-2]) == 6]

# a = [f"{path}{i}.obj" for i in a]

for i in a:
    with open(i, "rb") as f:
        o = pickle.load(f)
    print(o.keys())
