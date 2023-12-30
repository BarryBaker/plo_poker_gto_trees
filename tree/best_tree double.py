import pandas as pd
import numpy as np
import pickle
import os
from icecream import ic as qw
import time

with open("a.obj", "rb") as f:
    strat = pickle.load(f)

actions = ["C", "R50"]
strat["best_action"] = strat[actions].idxmax(axis=1)
tree_action = strat[actions].idxmax(axis=1)

# count = strat.shape[0]


def step(df: pd.DataFrame, hand_before=[], level2=False):
    if df.shape[0] == 0:
        return
    a = df.copy()

    init_action = a["best_action"].value_counts().idxmax()
    a["action"] = init_action

    if len(hand_before) > 0:
        dd = pd.DataFrame([strat[i[0]] == i[1] for i in hand_before])
        # qw(init_action)
        tree_action[(dd.transpose().all(axis=1))] = init_action

    max_score = (
        a.apply(
            lambda row: sorted([row[i] for i in actions])[-2]
            - sorted([row[i] for i in actions])[-1],
            axis=1,
        ).sum()
        / a.shape[0]
    )

    a["loss"] = a.apply(
        lambda row: sorted(
            [row[i] for i in actions if i != row["action"]]
        )[-1]
        - row[row["action"]],
        axis=1,
    )

    loss = sum(a.loss) / a.shape[0]

    if loss == max_score:
        return
    qw(a.sample(20))
    result = []
    hands = [
        i
        for i in a.columns
        if i not in [*actions, "action", "loss", "best_action"]
    ]
    for hand in hands:
        for tf in [0, 1]:
            filtered = a[a[hand] == tf]

            if filtered.shape[0] > 0:
                result.append(
                    (hand, tf, sum(a["loss"][a[hand] == tf]) / a.shape[0])
                )

    result = sorted(result, key=lambda x: x[2], reverse=True)
    best_cut = result[0]
    loss_decr = round(best_cut[2] / (loss - max_score) * 100, 3)

    qw(hand_before, level2)
    qw(result[:5])

    if loss_decr > 2:
        qw("  " * sum([i[1] for i in hand_before]) + best_cut[0])
        step(
            a[a[best_cut[0]]],
            hand_before + [(best_cut[0], 1)],
        )

        step(
            a[~a[best_cut[0]]],
            hand_before + [(best_cut[0], 0)],
        )
    if not level2:
        step(
            a[a[best_cut[0]] == best_cut[1]],
            hand_before + [(best_cut[0], best_cut[1])],
            True,
        )


step(strat)

strat["tree_action"] = tree_action

# qw(strat.sample(20))
# qw(strat["best_action"].value_counts())
# qw(strat["tree_action"].value_counts())

df = pd.DataFrame(
    {
        "a": strat["best_action"],
        "b": strat["tree_action"],
    }
)
# qw(pd.crosstab(df["a"], df["b"]))
