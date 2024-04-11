import pandas as pd
import numpy as np
import pickle
import multiprocessing

from collections import Counter
from functools import reduce

from itertools import combinations
from time import time

# from icecream import ic as qw
from tqdm import tqdm

from tree.load_strat import (
    load_strat,
    get_boards,
    convert_action_name,
    gto_path,
)

from tree._utils import get_result


def step(
    df: pd.DataFrame,
    strat,
    actions,
    line,
    hand_before=[],
):
    a = df.copy()
    range_weight = a.shape[0] / strat.shape[0]
    # qw(range_weight)
    a.drop(
        [
            c
            for c in [i for i in a.columns if i not in actions + ["action"]]
            if (np.all(a[c]) or np.all(~a[c]))
        ],
        axis=1,
        inplace=True,
    )

    current_action = np.unique(a["action"])
    if len(current_action) > 1:
        raise Exception("Multiple action options in iterate step")
    current_action = current_action[0]
    other_actions = [j for j in actions if j != current_action]

    for i in other_actions:
        a[f"{i}_gain"] = a[i] - a[current_action]

    # print(a.iloc[:, [0, 1, 2, 3, 4, -3, -2, -1]].sample(20))

    result = []
    hands = [
        i
        for i in a.columns
        if i not in [*actions, "action"] + [f"{j}_gain" for j in actions]
    ]
    for hand in hands:
        for tf in [0, 1]:
            filtered = a[a[hand] == tf]

            if filtered.shape[0] > 0:
                for action in other_actions:
                    filtresult = get_result(filtered, actions, line, False)
                    largest_action = max(filtresult, key=filtresult.get)

                    largest_value = filtresult[largest_action]
                    result.append(
                        (
                            hand,
                            tf,
                            sum(filtered[f"{action}_gain"]),
                            action,
                            largest_action,
                            largest_value,
                        )
                    )

    if len(result) == 0:
        return
    result = sorted(result, key=lambda x: x[2], reverse=True)
    # qw(current_action, hand_before, result[:10])

    best_cut = result[0]
    score_gain = best_cut[2]

    if score_gain >= min_gain * max_score / 100 * range_weight:
        append_tree(
            hand_before,
            best_cut[0],
        )

        a.loc[a[best_cut[0]] == best_cut[1], "action"] = best_cut[3]

        if len(hand_before) > 0:
            strat.loc[
                (strat[best_cut[0]] == best_cut[1])
                & pd.DataFrame([strat[i[0]] == i[1] for i in hand_before]).all(axis=0),
                "action",
            ] = best_cut[3]
        else:
            strat.loc[strat[best_cut[0]] == best_cut[1], "action"] = best_cut[3]

        step(
            a[a[best_cut[0]]],
            hand_before + [(best_cut[0], 1)],
        )

        step(
            a[~a[best_cut[0]]],
            hand_before + [(best_cut[0], 0)],
        )
    # if bestcut itself has mostly diferent action than current
    elif best_cut[4] != current_action and best_cut[5] > 60:
        append_tree(
            hand_before,
            best_cut[0],
        )

        a.loc[a[best_cut[0]] == best_cut[1], "action"] = best_cut[4]

        if len(hand_before) > 0:
            strat.loc[
                (strat[best_cut[0]] == best_cut[1])
                & pd.DataFrame([strat[i[0]] == i[1] for i in hand_before]).all(axis=0),
                "action",
            ] = best_cut[4]
        else:
            strat.loc[strat[best_cut[0]] == best_cut[1], "action"] = best_cut[4]

        step(
            a[a[best_cut[0]]],
            hand_before + [(best_cut[0], 1)],
        )

        step(
            a[~a[best_cut[0]]],
            hand_before + [(best_cut[0], 0)],
        )
    else:
        # if not do_doubles:
        #     return
        # Doubles

        two_largest = [v for k, v in get_result(a, actions, line).items()]
        second_largest = sorted(two_largest)[-2]
        weight = 100 * a.shape[0] / strat.shape[0]

        if second_largest / 100 * weight < split_strength_weights_2:
            return
        result = []
        for hand in combinations(hands, 2):
            for tf in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                filtered = a[(a[hand[0]] == tf[0]) & (a[hand[1]] == tf[1])]

                if filtered.shape[0] > 0:
                    for action in other_actions:
                        score_gain = sum(filtered[f"{action}_gain"])
                        if (
                            score_gain
                            >= min_gain * min_gain * max_score / 100 * range_weight
                        ):
                            result.append(
                                (
                                    hand,
                                    tf,
                                    score_gain,
                                    action,
                                )
                            )

        if len(result) == 0:
            if second_largest / 100 * weight < split_strength_weights_3:
                return
            result = []
            for hand in combinations(hands, 3):
                for tf in [
                    (0, 0, 0),
                    (0, 1, 0),
                    (1, 0, 0),
                    (1, 1, 0),
                    (0, 0, 1),
                    (0, 1, 1),
                    (1, 0, 1),
                    (1, 1, 1),
                ]:
                    filtered = a[
                        (a[hand[0]] == tf[0])
                        & (a[hand[1]] == tf[1])
                        & (a[hand[2]] == tf[2])
                    ]

                    if filtered.shape[0] > 0:
                        for action in other_actions:
                            score_gain = sum(filtered[f"{action}_gain"])
                            if (
                                score_gain
                                >= min_gain * min_gain * max_score / 100 * range_weight
                            ):
                                result.append(
                                    (
                                        hand,
                                        tf,
                                        score_gain,
                                        action,
                                    )
                                )
            # qw(result)
            if len(result) == 0:
                return
            result = sorted(result, key=lambda x: x[2], reverse=True)

            best_cut = result[0]
            score_gain = best_cut[2]

            most_common = Counter([j for i in result for j in i[0]]).most_common(1)[0][0]

            append_tree(hand_before, most_common)

            step(
                a[a[most_common]],
                hand_before + [(most_common, 1)],
            )

            step(
                a[~a[most_common]],
                hand_before + [(most_common, 0)],
            )

        result = sorted(result, key=lambda x: x[2], reverse=True)

        best_cut = result[0]
        score_gain = best_cut[2]

        most_common = Counter([j for i in result for j in i[0]]).most_common(1)[0][0]

        append_tree(hand_before, most_common)

        step(
            a[a[most_common]],
            hand_before + [(most_common, 1)],
        )

        step(
            a[~a[most_common]],
            hand_before + [(most_common, 0)],
        )
