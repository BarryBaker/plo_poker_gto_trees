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


print(split_lines_tostreets(["C", "C", "R50"]))
