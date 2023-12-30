import pandas as pd
import numpy as np
import pickle
import os
from icecream import ic as qw
import time
from itertools import combinations


with open("a.obj", "rb") as f:
    strat = pickle.load(f)

actions = ["C", "R50"]
# strat["best_action"] = strat[actions].idxmax(axis=1)
# tree_action = strat[actions].idxmax(axis=1)

init_action = strat[actions].idxmax(axis=1).value_counts().idxmax()
strat["action"] = init_action

max_score = (
    strat.apply(
        lambda row: sorted([row[i] for i in actions])[-2]
        - sorted([row[i] for i in actions])[-1],
        axis=1,
    ).sum()
    # / strat.shape[0]
)

qw(max_score)


def step(df: pd.DataFrame):
    a = df.copy()

    a["loss"] = a.apply(
        lambda row: sorted(
            [row[i] for i in actions if i != row["action"]]
        )[-1]
        - row[row["action"]],
        axis=1,
    )
    qw(a)
    loss = sum(a.loss)  # / a.shape[0]
    # qw(loss)

    if loss == max_score:
        return

    result = []
    hands = [
        i
        for i in a.columns
        if i not in [*actions, "action", "loss", "best_action"]
    ]
    for hand in hands:
        for tf in [0, 1]:
            filtered = a[a[hand] == tf]
            # if hand == "sdbl":

            #     qw(a[a[hand] == tf])
            if filtered.shape[0] > 0:
                result.append(
                    (
                        hand,
                        tf,
                        sum(a["loss"][a[hand] == tf]),
                    )  # / a.shape[0])
                )

    result = sorted(result, key=lambda x: x[2], reverse=True)
    best_cut = result[0]
    loss_decrease = round(2 * best_cut[2] / (loss - max_score) * 100, 2)

    qw(result[:5])
    qw(loss_decrease)
    if loss_decrease > 0:
        a.loc[a[best_cut[0]] == best_cut[1], "action"] = a["action"].apply(
            lambda x: [i for i in actions if i != x][0]
        )
        step(a)
    else:
        # Doubles
        result = []
        for hand in combinations(hands, 2):
            for tf in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                filtered = a[(a[hand[0]] == tf[0]) & (a[hand[1]] == tf[1])]
                # if hand == "sdbl":

                #     qw(a[a[hand] == tf])
                if filtered.shape[0] > 0:
                    result.append(
                        (
                            hand,
                            tf,
                            sum(filtered["loss"]),
                        )  # / a.shape[0])
                    )
        result = sorted(result, key=lambda x: x[2], reverse=True)
        best_cut = result[0]
        loss_decrease = round(
            2 * best_cut[2] / (loss - max_score) * 100, 2
        )
        qw(result[:5])
        qw(loss_decrease)


step(strat)

# strat["tree_action"] = tree_action


# df = pd.DataFrame(
#     {
#         "a": strat["best_action"],
#         "b": strat["tree_action"],
#     }
# )
# qw(pd.crosstab(df["a"], df["b"]))
