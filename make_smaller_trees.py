import glob
import os
from icecream import ic as qw
import shutil
import json
import gzip
from omaha._cards import Board
from pprint import pprint
import time

from pprint import pprint

path = "/Users/barrybaker/Documents/blackcard2/trees_backup/blaccard_7_smallers/"
a = glob.glob(
    f"{path}*",
)
for fname in a:
    if "gz" in fname:
        with gzip.open(fname, "rb") as f:
            d = json.loads(f.read())
    else:
        with open(fname) as json_data:
            d = json.load(json_data)
    # print(d[0])
    # time.sleep(30)

    for i in d:
        i["actions"] = [j for j in i["tree"]["base_action"]]

    def pruin(d: dict):
        for s in d:
            del d[s]["weight"]
            if len(d[s]["sub"]) == 0:
                d[s] = [list(d[s]["action"].values()), []]

            else:
                del d[s]["action"]
                d[s]["rest"] = list(d[s]["rest"]["action"].values())
                pruin(d[s]["sub"])

    def pruin2(d: dict):
        for s in d:
            if isinstance(d[s], dict):
                d[s] = (d[s]["rest"], d[s]["sub"])
                pruin2(d[s][1])

    for i in d:
        pruin(i["tree"]["ROOT"]["sub"])
        if len(i["tree"]["ROOT"]["sub"]) == 0:
            i["tree"]["ROOT"] = None
        else:
            i["tree"]["ROOT"]["rest"] = list(i["tree"]["ROOT"]["rest"]["action"].values())
            pruin2(i["tree"]["ROOT"]["sub"])
            i["tree"]["ROOT"] = (i["tree"]["ROOT"]["rest"], i["tree"]["ROOT"]["sub"])
            del i["tree"]["hide"]
        i["tree"]["base_action"] = list(i["tree"]["base_action"].values())
    fname = fname.replace(
        path, "/Users/barrybaker/Documents/blackcard2/blackcard_8/public/trees/"
    )
    # if ".gz" in fname:
    #     json_str = json.dumps(d) + "\n"  # 2. string (i.e. JSON)
    #     json_bytes = json_str.encode("utf-8")  # 3. bytes (i.e. UTF-8)

    #     with gzip.open(
    #         fname,
    #         "w",
    #     ) as fout:  # 4. fewer bytes (i.e. gzip)
    #         fout.write(json_bytes)
    # else:
    #     with open(
    #         fname,
    #         "w",
    #     ) as fp:
    #         json.dump(d, fp)
