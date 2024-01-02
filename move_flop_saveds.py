import glob
import os
from icecream import ic as qw
import shutil

path = "/Users/barrybaker/Documents/blackcard2/blackcard2_back/app/saved/"
a = glob.glob(
    f"{path}*.obj",
)
a = [i.replace(path, "").replace(".obj", "") for i in a]

a = [i for i in a if len(i.split("_")[-2]) == 6]
a = [f"{path}{i}.obj" for i in a]

for i in a:
    shutil.copyfile(i, i.replace("saved", "saved_new"))
