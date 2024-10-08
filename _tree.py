import pandas as pd
import numpy as np
import pickle
import multiprocessing
from scipy.stats import pointbiserialr

from collections import Counter
from functools import reduce

from itertools import combinations, product
from time import time
from icecream import ic as qw
from tqdm import tqdm


from tree.load_strat import load_strat, get_boards, gto_path, get_board_from_link
from tree.prun_tree import pruin_tree
from tree.url import Url, Line
from tree.skeleton import skeleton
from tree._utils import get_result, convert_action_name, detect_hero

from omaha._static import card_values, poslist
from omaha._cards import Board


def main(result_list, boards: list):
    for url in tqdm(boards):
        with open(url, "rb") as f:
            a = pickle.load(f)

        board = Url(url).board

        for line in a:

            is_attack = Line(line).is_attack
            strat_actions = load_strat(
                a[line],
                url,
            )
            strat_full, actions = strat_actions
            strat = strat_full.copy()
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
                            for c in [
                                i for i in a.columns if i not in actions + ["action"]
                            ]
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
                        if i
                        not in [*actions, "action"] + [f"{j}_gain" for j in actions]
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
                                    continue

                        return result

                    result = iter_step(1)

                    if len(result) == 0:
                        return
                    result = sorted(result, key=lambda x: abs(x[2]), reverse=True)

                    result_filtered = skeleton(
                        board,
                        hand_before,
                        result,
                        is_attack,
                        strat.columns,
                        Url(url).pot,
                    )
                    if result_filtered and len(result_filtered) > 0:

                        result = result_filtered

                    a_result = get_result(a, actions, line, False)
                    a_result_sort = sorted(
                        [(k, v) for k, v in a_result.items()],
                        key=lambda x: x[1],
                        reverse=True,
                    )

                    best_cut = result[0]

                    # bc_1_weight = a[a[best_cut[0]]].shape[0] / a.shape[0] * weight
                    bc_1_result = get_result(a[a[best_cut[0]]], actions, line, False)
                    bc_1_result_sort = sorted(
                        [(k, v) for k, v in bc_1_result.items()],
                        key=lambda x: x[1],
                        reverse=True,
                    )

                    # bc_0_weight = a[~a[best_cut[0]]].shape[0] / a.shape[0] * weight
                    bc_0_result = get_result(a[~a[best_cut[0]]], actions, line, False)
                    bc_0_result_sort = sorted(
                        [(k, v) for k, v in bc_0_result.items()],
                        key=lambda x: x[1],
                        reverse=True,
                    )

                    approved = not (bc_1_result_sort[0][0] == bc_0_result_sort[0][0])

                    append_tree(
                        hand_before, (best_cut[0], approved, weight * abs(best_cut[2]))
                    )

                    if best_cut[2] > 0:
                        a.loc[a[best_cut[0]], "action"] = best_cut[1]
                    else:
                        a.loc[~a[best_cut[0]], "action"] = best_cut[1]

                    step(
                        a[a[best_cut[0]]],
                        hand_before
                        + [((best_cut[0], approved, weight * abs(best_cut[2])), 1)],
                    )

                    step(
                        a[~a[best_cut[0]]],
                        hand_before
                        + [((best_cut[0], approved, weight * abs(best_cut[2])), 0)],
                    )
                    # return min_weight, min_action

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
                    level["sub"][keys[0]]["weight"] = (
                        a[a[keys[0]] == 1].shape[0] / whole
                    )
                else:
                    get_freqs(level["sub"][keys[0]], a[a[keys[0]] == 1])

                if len(keys) == 1:
                    return

                for key in keys[1:]:
                    filter_keys = keys[: keys.index(key) + 1]

                    if len(level["sub"][filter_keys[-1]]) == 0:
                        level["sub"][filter_keys[-1]]["action"] = get_result(
                            a[
                                pd.DataFrame([a[j] == 0 for j in filter_keys[:-1]]).all(
                                    axis=0
                                )
                                & (a[filter_keys[-1]] == 1)
                            ],
                            actions,
                            line,
                        )
                        level["sub"][filter_keys[-1]]["rest"] = {}
                        level["sub"][filter_keys[-1]]["sub"] = {}
                        level["sub"][filter_keys[-1]]["weight"] = (
                            a[
                                pd.DataFrame([a[j] == 0 for j in filter_keys[:-1]]).all(
                                    axis=0
                                )
                                & (a[filter_keys[-1]] == 1)
                            ].shape[0]
                            / whole
                        )
                    else:
                        get_freqs(
                            level["sub"][filter_keys[-1]],
                            a[
                                pd.DataFrame([a[j] == 0 for j in filter_keys[:-1]]).all(
                                    axis=0
                                )
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

            situ = f"{url.replace(gto_path,'').replace('.obj','_')}{line}"
            situ = situ.split("_")

            if len(situ) == 6:
                result = {
                    "stack": situ[0],
                    "poss": f"{situ[1]}_{situ[2]}",
                    "pot": situ[3],
                    "board": situ[4],
                    "line": situ[5],
                    "tree": final_tree,
                    "layer": "flop" if len(situ[4]) == 6 else "turn",
                    "hero": detect_hero(f"{situ[1]}_{situ[2]}", situ[5]),
                }

            if len(situ) == 7:
                result = {
                    "stack": situ[0],
                    "poss": f"{situ[1]}_{situ[2]}_{situ[3]}",
                    "pot": situ[4],
                    "board": situ[5],
                    "line": situ[6],
                    "tree": final_tree,
                    "layer": "flop" if len(situ[5]) == 6 else "turn",
                    "hero": detect_hero(f"{situ[1]}_{situ[2]}_{situ[3]}", situ[6]),
                }

            result_list.append(result)


for p in [
    ("BTN_BB", "SRP"),
    ("MP_BB", "SRP"),
    ("SB_BB", "SRP"),
    ("CO_BTN", "SRP"),
    ("EP_BTN", "SRP"),
    ("SB_BB", "3BP"),
    ("CO_BTN", "3BP"),
    ("EP_CO", "3BP"),
    ("BTN_SB", "3BP"),
    ("CO_SB", "3BP"),
    ("MP_SB", "3BP"),
]:
    filters = {
        "poss": [
            p[0],
        ],
        "pot": [p[1]],
    }
    all_urls = get_boards(filters)

    """----------------"""
    num_chunks = 9
    avg_chunk_size = len(all_urls) // num_chunks
    remainder = len(all_urls) % num_chunks

    chunks = []
    start = 0
    for i in range(num_chunks):
        end = start + avg_chunk_size + (1 if i < remainder else 0)
        chunks.append(all_urls[start:end])
        start = end
    """----------------"""

    if __name__ == "__main__":
        manager = multiprocessing.Manager()
        shared_list = manager.list()
        processes = []
        if len(chunks) <= 9:
            for i in chunks:
                process = multiprocessing.Process(target=main, args=(shared_list, i))
                process.start()
                processes.append(process)

            for process in processes:
                process.join()

            result = list(shared_list)

            result = sorted(
                result, key=lambda x: card_values[x["board"][6]], reverse=True
            )
            result = sorted(
                result, key=lambda x: card_values[x["board"][4]], reverse=True
            )
            result = sorted(
                result, key=lambda x: card_values[x["board"][2]], reverse=True
            )
            result = sorted(
                result, key=lambda x: card_values[x["board"][0]], reverse=True
            )

            grouped_result = {}

            for type in [
                [False, False, False, False],
                [False, False, True, False],
                [True, False, False, False],
                [True, False, True, False],
                [False, True, False, False],
                [False, True, True, False],
                [False, False, False, True],
            ]:
                for hero in poslist:
                    filename = None
                    for i in result:
                        if i["hero"] == hero and (
                            (
                                type[3]
                                and (len(Board(i["board"][:6]).flush) > 0) == type[3]
                            )
                            or (
                                not type[3]
                                and Board(i["board"][:6]).is_paired == type[0]
                                and (len(Board(i["board"][:6]).str8) > 0) == type[1]
                                and (len(Board(i["board"][:6]).fd) > 0) == type[2]
                                and (len(Board(i["board"][:6]).flush) == 0)
                            )
                        ):
                            filename = f"100_{filters['poss'][0]}_{filters['pot'][0]}_{type[0]}_{type[1]}_{type[2]}_{type[3]}_turn_{hero}"

                            if filename in grouped_result:
                                grouped_result[filename].append(i)
                            else:
                                grouped_result[filename] = [i]
