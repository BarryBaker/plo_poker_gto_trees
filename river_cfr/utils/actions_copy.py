actions = {
    "": ["C", "R100"],
    "C-R100": ["F", "C", "A"],
    "C": ["C", "R100"],
    "R100": ["F", "C", "A"],
    "R100-A": ["F", "C"],
    "C-R100-A": ["F", "C"],
}
terminals = [
    "R100-F",
    "R100-C",
    "C-C",
    "C-R100-C",
    "C-R100-F",
    "R100-A-F",
    "R100-A-C",
    "C-R100-A-F",
    "C-R100-A-C",
]


def payoff(history, cards):
    if history == "R100-F":
        return [22, -22]
    elif history == "C-R100-F":
        return [-22, 22]
    elif history == "R100-A-F":
        return [-67, 67]
    elif history == "C-R100-A-F":
        return [67, -67]

    if cards[0] < cards[1]:
        winner = [1, -1]
    elif cards[0] > cards[1]:
        winner = [-1, 1]
    else:
        return [1, 1]

    if history == "C-C":
        return [-22 if i < 0 else 22 for i in winner]
    if history in ["R100-C", "C-R100-C"]:
        return [-67 if i < 0 else 67 for i in winner]
    else:
        # print(5, "  ", (time.time() - start_time))
        return [-100 if i < 0 else 100 for i in winner]
