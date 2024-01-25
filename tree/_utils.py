import pandas as pd


def convert_action_name(action, line):
    # if line == "":
    #     return ""
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


def get_result(a: pd.DataFrame, actions, line, convert=True):
    result = {i: a[i].sum() for i in actions}
    all_sum = sum([result[i] for i in result])

    for i in result:
        result[i] = round(result[i] / all_sum * 100)

    if convert:
        return {convert_action_name(k, line): v for k, v in result.items()}
    return result
