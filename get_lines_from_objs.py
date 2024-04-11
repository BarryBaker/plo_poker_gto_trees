import glob
from tqdm import tqdm
import pickle


gto_path = "/Users/barrybaker/Documents/fromAHK/objs3/"
files = glob.glob(f"{gto_path}*.obj")

the_filters = []

for link in tqdm(files):
    with open(link, "rb") as f:
        a = pickle.load(f)
        lines = [j for j in a]
        splitted = link.replace(gto_path, "").split("_")
        board = splitted[-1].replace(".obj", "")
        pot = splitted[-2]
        stack = splitted[0]
        poss = splitted[1:-2]
        the_filters.append([stack, poss, pot, board, lines])
# print(the_filters)
with open(
    "alllinesfilter.obj",
    "wb",
) as fp:
    pickle.dump(the_filters, fp)
