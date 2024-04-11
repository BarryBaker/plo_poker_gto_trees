import os
from itertools import chain

data = "/Users/barrybaker/Documents/fromAHK/data/"
paths = (
    # "100_BTN_BB_SRP",
    # "100_MP_BB_SRP",
    # "100_BTN_SB_3BP",
    "100_CO_BTN_3BP",
    # "100_CO_BTN_SRP",
    # "100_CO_SB_3BP",
    # "100_EP_BTN_SRP",
    # "100_EP_CO_3BP",
    # "100_MP_SB_3BP",
    # "100_SB_BB_3BP",
    # "100_SB_BB_SRP",
)


def find_ahks(subline: str) -> list:
    return [
        f"{path}/{i}"
        for path, subdirs, files in chain.from_iterable(
            os.walk(data + path) for path in paths
        )
        for i in files
        if i.endswith(".ahk") and subline in i
    ]
