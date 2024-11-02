import pandas as pd
import numpy as np
import json

import sys
from scipy.stats import pointbiserialr
import warnings

from functools import reduce

from itertools import combinations, product


from tree.load_strat import load_strat
from tree.prun_tree import pruin_tree
from tree.url import Line
from tree.skeleton import skeleton
from tree._utils import get_result
from utils import merge_csvs

from omaha._static import card_values, poslist
from omaha._cards import Board


def main(*csvs):

    reference_parts = csvs[0].split("_")[:-1]  # All but the last part

    # Check that all files match the reference in all parts except the last
    for file in csvs[1:]:
        file_parts = file.split("_")[:-1]  # All but the last part
        if file_parts != reference_parts:
            raise ValueError(
                f"File names do not match except for the last element: {file}"
            )

    board = reference_parts[-3]
    line = reference_parts[-2]
    pot = reference_parts[-4]

    strat = merge_csvs(csvs)

    is_attack = Line(line).is_attack
    strat, actions = load_strat(
        strat,
        board,
    )

    strat = strat[strat[actions].max(axis=1) > 0]

    tree = {}
    if len(actions) > 1:

        init_action = strat[actions].idxmax(axis=1).value_counts().idxmax()
        strat["action"] = init_action

        def append_tree(hand_before, hand):
            keys = [i[0] for i in hand_before if i[1] == 1]
            if len(keys) == 0:
                tree[hand] = {}
            else:
                reduce(lambda x, y: x[y], [tree] + keys)[hand] = {}

        def step(df: pd.DataFrame, hand_before):
            a = df.copy()
            weight = a.shape[0] / strat.shape[0]

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

            hands = [
                i
                for i in a.columns
                if i not in [*actions, "action"] + [f"{j}_gain" for j in actions]
            ]

            def iter_step(col_cnt):
                result = []
                for hand in combinations(hands, col_cnt):
                    # print(hand)
                    for action in other_actions:
                        if a.shape[0] < 3:
                            continue
                        try:
                            with warnings.catch_warnings():
                                # Raise all warnings as exceptions
                                warnings.simplefilter("error")
                                corr_coefficient, p_value = pointbiserialr(
                                    a[hand[0]], a[f"{action}_gain"]
                                )
                                # print((hand[0], action, corr_coefficient))
                                result.append((hand[0], action, corr_coefficient))
                        except Warning as e:
                            continue

                return result

            result = iter_step(1)
            if len(result) == 0:
                return
            result = sorted(result, key=lambda x: abs(x[2]), reverse=True)

            result_filtered = skeleton(
                Board(board),
                hand_before,
                result,
                is_attack,
                strat.columns,
                pot,
            )
            if result_filtered and len(result_filtered) > 0:

                result = result_filtered

            best_cut = result[0]

            bc_1_result = get_result(a[a[best_cut[0]]], actions, line, False)
            bc_1_result_sort = sorted(
                [(k, v) for k, v in bc_1_result.items()],
                key=lambda x: x[1],
                reverse=True,
            )

            bc_0_result = get_result(a[~a[best_cut[0]]], actions, line, False)
            bc_0_result_sort = sorted(
                [(k, v) for k, v in bc_0_result.items()],
                key=lambda x: x[1],
                reverse=True,
            )

            approved = not (bc_1_result_sort[0][0] == bc_0_result_sort[0][0])

            append_tree(hand_before, (best_cut[0], approved, weight * abs(best_cut[2])))

            if best_cut[2] > 0:
                a.loc[a[best_cut[0]], "action"] = best_cut[1]
            else:
                a.loc[~a[best_cut[0]], "action"] = best_cut[1]

            step(
                a[a[best_cut[0]]],
                hand_before + [((best_cut[0], approved, weight * abs(best_cut[2])), 1)],
            )

            step(
                a[~a[best_cut[0]]],
                hand_before + [((best_cut[0], approved, weight * abs(best_cut[2])), 0)],
            )

        step(strat, [])

    tree = pruin_tree(tree)

    whole = strat.shape[0]

    def get_freqs(level: dict, a: pd.DataFrame):
        keys = list(level.keys())

        level["sub"] = level.copy()

        # Rest, action, weight
        none_of_keys = a[pd.DataFrame([a[j] == 0 for j in keys]).all(axis=0)]
        level["rest"] = {}
        level["rest"]["action"] = get_result(
            none_of_keys,
            actions,
            line,
        )
        level["rest"]["weight"] = none_of_keys.shape[0] / whole
        level["action"] = get_result(a, actions, line)
        level["weight"] = a.shape[0] / whole
        # ---------
        for key in keys:
            del level[key]

        if len(level["sub"][keys[0]]) == 0:
            level["sub"][keys[0]]["action"] = get_result(
                a[a[keys[0]] == 1], actions, line
            )
            level["sub"][keys[0]]["rest"] = {}
            level["sub"][keys[0]]["sub"] = {}
            level["sub"][keys[0]]["weight"] = a[a[keys[0]] == 1].shape[0] / whole
        else:
            get_freqs(level["sub"][keys[0]], a[a[keys[0]] == 1])

        if len(keys) == 1:
            return

        for key in keys[1:]:
            filter_keys = keys[: keys.index(key) + 1]

            if len(level["sub"][filter_keys[-1]]) == 0:
                level["sub"][filter_keys[-1]]["action"] = get_result(
                    a[
                        pd.DataFrame([a[j] == 0 for j in filter_keys[:-1]]).all(axis=0)
                        & (a[filter_keys[-1]] == 1)
                    ],
                    actions,
                    line,
                )
                level["sub"][filter_keys[-1]]["rest"] = {}
                level["sub"][filter_keys[-1]]["sub"] = {}
                level["sub"][filter_keys[-1]]["weight"] = (
                    a[
                        pd.DataFrame([a[j] == 0 for j in filter_keys[:-1]]).all(axis=0)
                        & (a[filter_keys[-1]] == 1)
                    ].shape[0]
                    / whole
                )
            else:
                get_freqs(
                    level["sub"][filter_keys[-1]],
                    a[
                        pd.DataFrame([a[j] == 0 for j in filter_keys[:-1]]).all(axis=0)
                        & (a[filter_keys[-1]] == 1)
                    ],
                )

    if len(tree) > 0:
        get_freqs(tree, strat)

    base_action = get_result(strat, actions, line)

    if len(tree) > 0:
        del tree["action"]
        del tree["weight"]

        final_tree = {
            "ROOT": tree,
            "base_action": base_action,
            "hide": False,
        }

    else:
        final_tree = {
            "ROOT": {
                "rest": {},
                "sub": {},
            },
            "base_action": base_action,
            "hide": False,
        }

    return final_tree


if __name__ == "__main__":
    if len(sys.argv) < 2:
        file_paths = [
            "PLO500_100_6_BTN_BB_SRP_Ks7d5d_C_BTN_CHECK.csv",
            "PLO500_100_6_BTN_BB_SRP_Ks7d5d_C_BTN_RAISE75.csv",
        ]

    else:
        file_paths = sys.argv[1:]

    result = main(*file_paths)

    def clean_dict(data):
        # Recursively process the dictionary
        if isinstance(data, dict):
            cleaned_data = {}
            for k, v in data.items():

                if k == "hide":
                    continue
                if isinstance(v, dict) and v:  # Process non-empty dictionaries
                    # Special handling for 'sub' key: elevate its contents one level higher
                    if k == "sub":
                        cleaned_sub_dict = clean_dict(v)  # Clean the 'sub' dictionary
                        for sub_k, sub_v in cleaned_sub_dict.items():
                            cleaned_data[sub_k] = sub_v
                    else:
                        cleaned_sub_dict = clean_dict(v)
                        if cleaned_sub_dict:  # Only keep non-empty results
                            cleaned_data[k] = cleaned_sub_dict
                elif isinstance(v, dict):  # Skip empty dictionaries
                    continue
                elif k == "weight" and isinstance(
                    v, (int, float)
                ):  # Convert weight to percentage
                    cleaned_data[k] = f"{v * 100:.2f}%"
                else:
                    cleaned_data[k] = v
            return cleaned_data
        return data

    cleaned_data = clean_dict(result)

    print("Resulting directory:", json.dumps(cleaned_data, indent=4))
