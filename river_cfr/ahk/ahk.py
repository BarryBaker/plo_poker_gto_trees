import os

import pandas as pd

if __name__ == "__main__":
    from line import Line
    from static import poslist
else:
    from .line import Line
    from .static import poslist

wd = os.getcwd()


class Ahk:
    def __init__(self, ahk) -> None:
        self._ahk = ahk

        self.splitted_name = ahk.split("ahks/")[1].replace(".ahk", "").split("_")

    @property
    def data(self):
        # with open(f"{wd}/{self._ahk}.ahk") as f:
        with open(self._ahk) as f:
            return f.read()

    @property
    def line(self):
        return Line(self.splitted_name[-1])

    @property
    def board(self):
        board = self.splitted_name[6]
        return [board[i : i + 2] for i in range(0, len(board), 2)]

    @property
    def spr(self):
        pot = self.splitted_name[5]
        spr_start = None
        if pot == "SRP":
            spr_start = 96.5 / 8
        if pot == "3BP":
            spr_start = 88.5 / 24
        pot_end = self.line.pot
        stacks_end = (pot_end - 1) / 2
        return (spr_start - stacks_end) / pot_end

    @property
    def players(self):
        if poslist.index(self.splitted_name[4]) > poslist.index(self.splitted_name[3]):
            return [self.splitted_name[4], self.splitted_name[3]]
        return [self.splitted_name[3], self.splitted_name[4]]

    @property
    def ranges(self):
        s1 = self.data.split("r1 := ")
        stringRanges = [i.split("Clipboard = ")[0] for i in s1[1:]]
        ranges = {}

        for playernr, stringRange in enumerate(stringRanges):
            strippedRange = stringRange.replace('"' + "\n", "").replace('"', "")
            stripped = strippedRange.split("r")
            result = ""
            for i in stripped:
                if " := " in i:
                    result = result + i.split(" := ")[1]
                else:
                    result = result + i
            resultList = result.split(",")

            resultTuples = [i.split("@") for i in resultList]

            resultDf = pd.DataFrame(resultTuples, columns=["combo", "weight"])
            resultDf = resultDf.set_index("combo")

            a = resultDf.astype("int")
            # TODO check if df is empty
            ranges[self.players[playernr]] = a[a.weight > 50]
        return ranges

    def ranges_discarded(self, card):
        return {
            i: self.ranges[i].loc[self.ranges[i].index.map(lambda x: card not in x)]
            for i in self.ranges
        }
