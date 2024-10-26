import pandas as pd
from omaha._static import poslist


def convert_action_name(action, line):
    if action == "C":
        if line == "" or line[-1] == "C":
            return "CHECK"
        return "CALL"
    if action[0] == "R":
        return f"RAISE{action[1:]}"
    return {
        "F": "FOLD",
        "C": "CALL",
        "MIN": "MIN",
        "MR": "MIN",
        "A": "ALLIN",
    }[action]


def get_result(a: pd.DataFrame, actions, line, convert=False):
    result = {i: a[i].sum() for i in actions}
    all_sum = sum([result[i] for i in result])

    for i in result:
        result[i] = round(result[i] / all_sum * 100)

    if convert:
        return {convert_action_name(k, line): v for k, v in result.items()}
    return result


def split_lines_tostreets(line: list[str]):
    cs = [i for i in line if i == "C"]
    if len(cs) == 0 or (len(cs) == 1 and line[0] == "C"):
        return line, []

    if line[0] == "C":
        otherC = [k for k, n in enumerate(line) if n == "C"][1]
    else:
        otherC = [k for k, n in enumerate(line) if n == "C"][0]
    flopLine = line[: otherC + 1]
    turnLine = line[otherC + 1 :]
    if len(turnLine) == 0:
        turnLine = [""]
    return flopLine, turnLine


def detect_hero(poss: str, line: str):
    poss = poss.split("_")
    if len(poss) == 2:
        flopLine, turnLine = split_lines_tostreets(line.split("-"))
        pos1isIp = poslist.index(poss[0]) > poslist.index(poss[1])

        line = turnLine if len(turnLine) > 0 else flopLine

        action_count = len(line)
        if line[0] == "":
            action_count = 0

        if pos1isIp and action_count % 2 == 0 or not pos1isIp and action_count % 2 == 1:
            return poss[1]
        return poss[0]

    line = line.split("-")
    byPos = None
    if poss[0] == "CO":
        if poss[2] == "BB":
            byPos = ["BB", "CO", "BTN"]
        else:
            byPos = ["SB", "CO", "BTN"]
    if poss[0] == "MP":
        byPos = ["MP", "CO", "BTN"]
    if poss[0] == "EP":
        byPos = ["EP", "CO", "BTN"]

    if "F" in line and line.index("F") < len(line) - 2:
        lineUntilFold = line[: line.index("F") + 1]
        lineAfterfold = line[line.index("F") + 1 :]
        linsAsNormal = lineUntilFold + lineAfterfold[:1]
        if len(linsAsNormal) % 3 == 0:
            lastacctionsNormal = [
                byPos[0],
                byPos[1],
                byPos[2],
            ]
        elif len(linsAsNormal) % 3 == 1:
            lastacctionsNormal = [
                byPos[1],
                byPos[2],
                byPos[0],
            ]
        else:
            lastacctionsNormal = [
                byPos[2],
                byPos[0],
                byPos[1],
            ]
        if len(lineAfterfold) % 2 == 0:
            return lastacctionsNormal[2]

        else:
            return lastacctionsNormal[0]

    if line[0] == "":
        return byPos[0]
    return byPos[len(line) % 3]
