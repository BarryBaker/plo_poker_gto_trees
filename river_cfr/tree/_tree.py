import pandas as pd
import numpy as np
import pickle
import multiprocessing
from scipy.stats import pointbiserialr
import json

from collections import Counter
from functools import reduce

from itertools import combinations, product
from time import time

# from icecream import ic as qw
from tqdm import tqdm
import gzip
import warnings

warnings.filterwarnings("error")

from .tree.load_strat import load_strat  # , get_boards, gto_path, get_board_from_link
from .tree.prun_tree import pruin_tree

# from .tree.url import Url, Line
# from .tree.skeleton import skeleton
from .tree._utils import get_result  # , convert_action_name, detect_hero

# from .omaha._static import card_values, poslist
# from .omaha._cards import Board


#'100_BTN_SB_3BP_Th8h8d6c'
def pruin(d: dict):
    for s in d:
        del d[s]["weight"]
        if len(d[s]["sub"]) == 0:
            d[s] = [list(d[s]["action"].values()), []]

        else:
            del d[s]["action"]
            d[s]["rest"] = list(d[s]["rest"]["action"].values())
            pruin(d[s]["sub"])


def pruin2(d: dict):
    for s in d:
        if isinstance(d[s], dict):
            d[s] = (d[s]["rest"], d[s]["sub"])
            pruin2(d[s][1])


def build_tree(strat, board, line):
    strat_actions = load_strat(strat, board)

    strat_full, actions = strat_actions
    strat = strat_full.copy()
    strat = strat[strat[actions].max(axis=1) > 0]

    tree = {}
    if len(actions) > 1:
        # max_scores = strat[actions].max(axis=1)
        # max_score = max_scores.sum()

        init_action = strat[actions].idxmax(axis=1).value_counts().idxmax()
        strat["action"] = init_action
        # init_score = strat[init_action].sum()

        def append_tree(hand_before, hand):
            keys = [i[0] for i in hand_before if i[1] == 1]
            if len(keys) == 0:
                tree[hand] = {}
            else:
                reduce(lambda x, y: x[y], [tree] + keys)[hand] = {}

        def step(df: pd.DataFrame, hand_before):
            a = df.copy()
            weight = a.shape[0] / strat.shape[0]
            bools = [
                c
                for c in [i for i in a.columns if i not in actions + ["action"]]
                if (a[c].dtype == "bool")
            ]

            # print(bools)
            # if len(bools) > 0:
            a.drop(
                [c for c in bools if (np.all(a[c]) or np.all(~a[c]))],
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
                    for action in other_actions:
                        try:
                            corr_coefficient, p_value = pointbiserialr(
                                a[hand[0]], a[f"{action}_gain"]
                            )
                            result.append((hand[0], action, corr_coefficient))
                        except Exception as e:
                            # print(e)
                            # print(a[f"{action}_gain"])
                            continue

                return result

            result = iter_step(1)

            if len(result) == 0:
                return
            result = sorted(result, key=lambda x: abs(x[2]), reverse=True)

            # result_filtered = skeleton(
            #     board, hand_before, result, is_attack, strat.columns, Url(url).pot
            # )
            # if result_filtered and len(result_filtered) > 0:
            #     # print(result_filtered)
            #     result = result_filtered

            # a_result = get_result(a, actions, line, False)
            # a_result_sort = sorted(
            #     [(k, v) for k, v in a_result.items()],
            #     key=lambda x: x[1],
            #     reverse=True,
            # )

            best_cut = result[0]

            bc_1_weight = a[a[best_cut[0]]].shape[0] / a.shape[0] * weight
            bc_1_result = get_result(a[a[best_cut[0]]], actions, line, False)
            bc_1_result_sort = sorted(
                [(k, v) for k, v in bc_1_result.items()],
                key=lambda x: x[1],
                reverse=True,
            )

            bc_0_weight = a[~a[best_cut[0]]].shape[0] / a.shape[0] * weight
            bc_0_result = get_result(a[~a[best_cut[0]]], actions, line, False)
            bc_0_result_sort = sorted(
                [(k, v) for k, v in bc_0_result.items()],
                key=lambda x: x[1],
                reverse=True,
            )

            approved = not (bc_1_result_sort[0][0] == bc_0_result_sort[0][0])

            append_tree(hand_before, (best_cut[0], approved, weight * abs(best_cut[2])))
            # if hand_before_hands == []:
            #     print(board, line, tree)

            if best_cut[2] > 0:
                a.loc[a[best_cut[0]], "action"] = best_cut[
                    1
                ]  # ami besc cut filternel a leggyakoribb action\
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
            # return min_weight, min_action

        step(strat, [])

    # def count(prod, c=0):
    #     for mykey in prod:
    #         if isinstance(prod[mykey], dict):
    #             # calls repeatedly
    #             c = count(prod[mykey], c + 1)
    #         else:
    #             c += 1
    #     return c

    # print(tree, count(tree))
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

    # print(board, line, tree)
    if len(tree) > 0:
        get_freqs(tree, strat)
    # else:
    #     print(board, line)
    # print("\n", "\n", tree)

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
    pruin(final_tree["ROOT"]["sub"])
    if len(final_tree["ROOT"]["sub"]) == 0:
        final_tree["ROOT"] = None
    else:
        final_tree["ROOT"]["rest"] = list(final_tree["ROOT"]["rest"]["action"].values())
        pruin2(final_tree["ROOT"]["sub"])
        final_tree["ROOT"] = (
            final_tree["ROOT"]["rest"],
            final_tree["ROOT"]["sub"],
        )
        del final_tree["hide"]
    final_tree["base_action"] = list(final_tree["base_action"].values())

    return final_tree
