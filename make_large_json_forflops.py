import glob
import os
from icecream import ic as qw
import shutil
import json
import gzip
from omaha._cards import Board

path = "/Users/barrybaker/Documents/blackcard2/blackcard_8/public/trees/"
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
    # if "50" not in i and "base" not in i:
    #     continue

    filename = i.replace(path, "").replace(".json", "")
    # if "base" in i:
    #     filename = filename.replace("_base", "")
    # print(filename)
    # with gzip.open(i, "rb") as f:
    #     data = json.loads(f.read())
    with open(i) as json_data:
        data = json.load(json_data)
    result[filename] = data
# print(result)

json_str = json.dumps(result) + "\n"  # 2. string (i.e. JSON)
json_bytes = json_str.encode("utf-8")  # 3. bytes (i.e. UTF-8)

with gzip.open(path + "flops.gz", "w") as fout:  # 4. fewer bytes (i.e. gzip)
    fout.write(json_bytes)
# for line in lines:
#     # print(line)
#     boards = [i["board"] for i in data if i["line"] == line]
#     btypes = list(set([boardtype(Board(i)) for i in boards]))
#     result[filename][line] = btypes
#     # print(btypes)
#     # for i in boards:
#     #     print(i, boardtype(Board(i)))
# filename = f"/Users/barrybaker/Documents/blackcard2/blackcard_8/public/"
# with open(
#     "basejsons.json",
#     "w",
# ) as fp:
#     json.dump(result, fp)
