import glob
import os
from icecream import ic as qw
import shutil
import json
import gzip
from omaha._cards import Board

path = "/Users/barrybaker/Documents/blackcard2/blackcard_6/public/trees/"
a = glob.glob(
    f"{path}*.json",
)
for i in a:
    if "gz" not in i and "100" in i:
        # print(i)
        with open(i, "rb") as f_in, gzip.open(
            i.replace(".json", "_base.json.gz"), "wb"
        ) as f_out:
            f_out.writelines(f_in)
    elif "gz" not in i:
        with open(i, "rb") as f_in, gzip.open(
            i.replace(".json", ".json.gz"), "wb"
        ) as f_out:
            f_out.writelines(f_in)


# def boardtype(b: Board) -> str:
#     if b.is_doublepaired:
#         return "dp"
#     if b.is_paired:
#         if b.is_flush:
#             return "pf"
#         if b.is_str8:
#             if b.is_suited:
#                 return "pss"
#             return "psr"
#         if b.is_suited:
#             return "ps"
#         return "pr"
#     if b.is_flush:
#         return "f"
#     if b.is_str8:
#         if b.is_suited:
#             return "uss"
#         return "usr"
#     if b.is_suited:
#         return "us"
#     return "ur"


# result = {}
# for i in a:
#     filename = i.replace(path, "").replace(".json.gz", "")
#     # print(filename)
#     result[filename] = {}
#     with gzip.open(i, "rb") as f:
#         data = json.loads(f.read())
#     lines = list(set([i["line"] for i in data]))

#     for line in lines:
#         # print(line)
#         boards = [i["board"] for i in data if i["line"] == line]
#         btypes = list(set([boardtype(Board(i)) for i in boards]))
#         result[filename][line] = btypes
#         # print(btypes)
#         # for i in boards:
#         #     print(i, boardtype(Board(i)))
# filename = f"/Users/barrybaker/Documents/blackcard2/blackcard_5/public/turnselector.json"
# with open(
#     filename,
#     "w",
# ) as fp:
#     json.dump(result, fp)
