import glob
import os
from icecream import ic as qw
import shutil
from tqdm import tqdm


path = "/Users/barrybaker/Documents/blackcard2/blackcard2_back/app/saved_hibrid/"
a = glob.glob(
    f"{path}*.obj",
)
a = [i.replace(path, "").replace(".obj", "") for i in a]

a = [i for i in a if len(i.split("_")[-2]) == 8]
a = [f"{path}{i}.obj" for i in a]

for i in tqdm(a):
    shutil.copyfile(i, i.replace("saved_hibrid", "saved"))
