poslist = ["SB", "BB", "EP", "MP", "CO", "BTN"]

card_values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

suit_values = {"s": 3, "h": 2, "d": 1, "c": 0}

card_values_inv = {v: k for k, v in card_values.items()}
suit_values_inv = {v: k for k, v in suit_values.items()}


def actions_order(action):
    if action[0] == "F":
        return 0
    if action[0] == "C":
        return 1
    if action[0] == "M":
        return 2

    if action[0] == "A":
        return 100
    return int(action.replace("RAISE", ""))
