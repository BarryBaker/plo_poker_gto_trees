import glob
import os
from icecream import ic as qw
import shutil
import json


path = "/Users/barrybaker/Documents/blackcard2/trees_backup/bigtrees/trees/"
a = glob.glob(
    f"{path}*",
)
for pot in ["SRP", "3BP"]:
    for pos in ["SB", "BB", "EP", "MP", "CO", "BTN"]:
        for street in ["flop", "turn"]:
            result = {}
            for file in a:
                if pot in file and f"{street}_{pos}" in file:
                    with open(file, "rb") as f:
                        o = json.load(f)
                    # print(file.replace(".json", "").replace(path, ""), [i["board"] for i in o])
                    result[file.replace(".json", "").replace(path, "")] = o
            # print(len(result))

            with open(
                path.replace("/trees/", "/") + f"alltrees_{pot}_{pos}_{street}.json",
                "w",
            ) as fp:
                json.dump(result, fp)

# print(a)
# a = [i.replace(path, "").replace(".obj", "") for i in a]
# a = [i for i in a if len(i.split("_")[-2]) == 6]

# a = [f"{path}{i}.obj" for i in a]

# newpath = "/Users/barrybaker/Documents/blackcard2/blackcard_newest/src/assets/trees/"
# for file in a:
#     with open(file, "rb") as f:
#         o = json.load(f)
#     if len(o) > 100:
#         num_chunks = 10

#         avg_chunk_size = len(o) // num_chunks
#         remainder = len(o) % num_chunks

#         chunks = []
#         start = 0
#         for i in range(num_chunks):
#             end = start + avg_chunk_size + (1 if i < remainder else 0)
#             chunks.append(o[start:end])
#             start = end
#     else:
#         chunks = [o]
#     for index, new in enumerate(chunks):
#         with open(
#             file.replace(path, newpath).replace(".json", f"_{index}.json"),
#             "w",
#         ) as fp:
# json.dump(new, fp)
