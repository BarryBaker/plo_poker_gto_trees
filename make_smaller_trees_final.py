import glob
import os
from icecream import ic as qw
import shutil
import json
import gzip
from omaha._cards import Board

path = "/Users/barrybaker/Documents/blackcard2/trees_backup/blaccard_7/"
a = glob.glob(
    f"{path}*",
)
# for i in a:
#     if "gz" not in i and "100" in i:
#         # print(i)
#         with open(i, "rb") as f_in, gzip.open(
#             i.replace(".json", "_base.json.gz"), "wb"
#         ) as f_out:
#             f_out.writelines(f_in)
#     elif "gz" not in i:
#         with open(i, "rb") as f_in, gzip.open(
#             i.replace(".json", ".json.gz"), "wb"
#         ) as f_out:
#             f_out.writelines(f_in)


result = {}
for i in a:
    if "100" in i and "flop" in i:
        if "gz" in i:
            filename = i.replace(path, "").replace(".json.gz", "")
            with gzip.open(i, "rb") as f:
                data = json.loads(f.read())
            if filename in result:
                result[filename] = result[filename] + data
            else:
                result[filename] = data
        else:
            filename = i.replace(path, "").replace(".json", "")
            with open(i) as json_data:
                data = json.load(json_data)
            if filename in result:
                result[filename] = result[filename] + data
            else:
                result[filename] = data
# for i in result:
#     print(i)
# print([i["line"] for i in result["100_CO_SB_3BP_False_False_False_False_flop_SB"]])

# for line in lines:
#     # print(line)
#     boards = [i["board"] for i in data if i["line"] == line]
#     btypes = list(set([boardtype(Board(i)) for i in boards]))
#     result[filename][line] = btypes
#     # print(btypes)
#     # for i in boards:
#     #     print(i, boardtype(Board(i)))

for i in result:
    filename = f"/Users/barrybaker/Documents/blackcard2/trees_backup/blaccard_7_smallers/{i}.json"

    with open(
        filename,
        "w",
    ) as fp:
        json.dump(result[i], fp)
