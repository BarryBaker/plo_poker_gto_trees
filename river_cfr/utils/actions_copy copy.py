actions = {
    "": ["X", "B"],
    "XB": ["F", "C", "R"],
    "X": ["X", "B"],
    "B": ["F", "C", "R"],
    "BR": ["F", "C"],
    "XBR": ["F", "C"],
}
terminals = ["BF", "BC", "XX", "XBC", "XBF", "BRF", "BRC", "XBRF", "XBRC"]


def payoff(history, cards):
    if history == "BF":
        return [22, -22]
    elif history == "XBF":
        return [-22, 22]
    elif history == "BRF":
        return [-67, 67]
    elif history == "XBRF":
        return [67, -67]

    if cards[0] < cards[1]:
        winner = [1, -1]
    elif cards[0] > cards[1]:
        winner = [-1, 1]
    else:
        return [1, 1]

    if history == "XX":
        return [-22 if i < 0 else 22 for i in winner]
    if history in ["BC", "XBC"]:
        return [-67 if i < 0 else 67 for i in winner]
    else:
        # print(5, "  ", (time.time() - start_time))
        return [-100 if i < 0 else 100 for i in winner]
