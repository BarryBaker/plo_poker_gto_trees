import pandas as pd
import numpy as np
import pickle
import os
from icecream import ic as qw
import time
from itertools import combinations
from collections import Counter
from functools import reduce
import json

with open("a.obj", "rb") as f:
    strat = pickle.load(f)

actions = ["C", "R50"]
# strat["best_action"] = strat[actions].idxmax(axis=1)
# tree_action = strat[actions].idxmax(axis=1)

max_score = strat.apply(
    lambda row: sorted([row[i] for i in actions])[-2]
    - sorted([row[i] for i in actions])[-1],
    axis=1,
).sum()

hand_count = strat.shape[0]

init_action = strat[actions].idxmax(axis=1).value_counts().idxmax()
strat["action"] = init_action

init_score = round(
    strat.apply(
        lambda row: sorted(
            [row[i] for i in actions if i != row["action"]]
        )[-1]
        - row[row["action"]],
        axis=1,
    ).sum()
    / max_score
    * 100,
    2,
)

tree = {}


def append_tree(hand_before, hand):
    keys = [i[0] for i in hand_before if i[1] == 1]
    if len(keys) == 0:
        tree[hand] = {}
    else:
        reduce(lambda x, y: x[y], [tree] + keys)[hand] = {}


def step(df: pd.DataFrame, hand_before=[]):
    a = df.copy()
    # a["action"] = a["best_action"].value_counts().idxmax()

    # if len(hand_before) > 0:
    #     dd = pd.DataFrame([strat[i[0]] == i[1] for i in hand_before])
    #     # qw(init_action)
    #     tree_action[(dd.transpose().all(axis=1))] = init_action

    max_score_filtered = (
        a.apply(
            lambda row: sorted([row[i] for i in actions])[-2]
            - sorted([row[i] for i in actions])[-1],
            axis=1,
        ).sum()
        # / a.shape[0]
    )
    # qw(max_score)

    a["loss"] = a.apply(
        lambda row: sorted(
            [row[i] for i in actions if i != row["action"]]
        )[-1]
        - row[row["action"]],
        axis=1,
    )

    loss = sum(a.loss)  # / a.shape[0]
    # print("\n\n")
    qw(hand_before)
    # qw(a)
    if loss == max_score_filtered:
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
    loss_decrease = -round(2 * best_cut[2] / max_score * 100, 3)

    # qw(best_cut, loss_decrease)

    if loss_decrease > 1:
        # qw("  " * sum([i[1] for i in hand_before]) + best_cut[0])
        append_tree(
            hand_before,
            best_cut[0],
            # "",  # [i for i in actions if i != a.action.iloc[0]][0],
        )

        a.loc[a[best_cut[0]] == best_cut[1], "action"] = a["action"].apply(
            lambda x: [i for i in actions if i != x][0]
        )
        if len(hand_before) > 0:
            strat.loc[
                (strat[best_cut[0]] == best_cut[1])
                & pd.DataFrame(
                    [strat[i[0]] == i[1] for i in hand_before]
                ).all(axis=0),
                "action",
            ] = strat["action"].apply(
                lambda x: [i for i in actions if i != x][0]
            )
        else:
            strat.loc[strat[best_cut[0]] == best_cut[1], "action"] = strat[
                "action"
            ].apply(lambda x: [i for i in actions if i != x][0])
        step(
            a[a[best_cut[0]]],
            hand_before + [(best_cut[0], 1)],
        )

        step(
            a[~a[best_cut[0]]],
            hand_before + [(best_cut[0], 0)],
        )
    else:
        # Doubles
        # qw("doubles", hand_before)
        result = []
        for hand in combinations(hands, 2):
            for tf in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                filtered = a[(a[hand[0]] == tf[0]) & (a[hand[1]] == tf[1])]

                if filtered.shape[0] > 0:
                    loss = sum(filtered["loss"])
                    if loss > 0:
                        result.append((hand, tf, loss))  # / a.shape[0])

        result = sorted(result, key=lambda x: x[2], reverse=True)
        result = [
            i
            for i in result
            if round(2 * i[2] / (loss - max_score) * 100, 3) > 1
        ]
        if len(result) == 0:
            return
        best_cut = result[0]
        loss_decrease = round(
            2 * best_cut[2] / (loss - max_score) * 100, 2
        )

        # qw(result)
        # qw(loss_decrease)
        most_common = Counter(
            [j for i in result for j in i[0]]
        ).most_common(1)[0][0]
        append_tree(hand_before, most_common)

        step(
            a[a[most_common]],
            hand_before + [(most_common, 1)],
        )

        step(
            a[~a[most_common]],
            hand_before + [(most_common, 0)],
        )


step(strat)


# print(tree)


def get_result(a: pd.DataFrame):
    result = {i: a[i].sum() for i in actions}
    all_sum = sum([result[i] for i in result])

    for i in result:
        result[i] = round(result[i] / all_sum * 100)
    return result


def get_freqs(level: dict, a: pd.DataFrame):
    keys = list(level.keys())

    # if len(keys) == 0:

    #     level = get_result(a)

    #     return

    # Rest
    level["rest"] = get_result(
        a[pd.DataFrame([a[j] == 0 for j in keys]).all(axis=0)]
    )
    if len(level[keys[0]]) == 0:
        level[keys[0]] = get_result(a[a[keys[0]] == 1])
    else:
        get_freqs(level[keys[0]], a[a[keys[0]] == 1])

    if len(keys) == 1:
        return

    for key in keys[1:]:
        filter_keys = keys[: keys.index(key) + 1]

        if len(level[filter_keys[-1]]) == 0:
            level[filter_keys[-1]] = get_result(
                a[
                    pd.DataFrame(
                        [a[j] == 0 for j in filter_keys[:-1]]
                    ).all(axis=0)
                    & (a[filter_keys[-1]] == 1)
                ]
            )
        else:
            get_freqs(
                level[filter_keys[-1]],
                a[
                    pd.DataFrame(
                        [a[j] == 0 for j in filter_keys[:-1]]
                    ).all(axis=0)
                    & (a[filter_keys[-1]] == 1)
                ],
            )


get_freqs(tree, strat)
print(json.dumps(tree, indent=2))

# qw(final_tree)
# qw(strat.sample(20))
# qw(strat["best_action"].value_counts())
# qw(strat["tree_action"].value_counts())

# df = pd.DataFrame(
#     {
#         "a": strat["best_action"],
#         "b": strat["tree_action"],
#     }
# )
# qw(pd.crosstab(df["a"], df["b"]))
