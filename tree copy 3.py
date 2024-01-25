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

from tree.load_strat import (
    load_strat,
    get_boards,
    gto_path,
)


from tree._utils import get_result, convert_action_name


#'100_BTN_SB_3BP_Th8h8d6c'

filters = {
    "poss": ["SB_BB"],  # "CO_SB", "MP_SB"],
    "pot": ["SRP"],
}
lines = ["C-C-C"]
# lines = [
# "C-C-C",
# "C-C-R33",
# "C-C-R75",
# "C-C-R50",
# "C-C-R100",
# "C-R50-C-C",
# "C-R33-C-C",
# "R50-C-C",
# "R33-C-C",
# "R50-C-R100",
# "R50-C-R50",
# "R50-C-R33",
# "R33-C-R50",
# "R33-C-R33",
# "C-C",
# "C-R50-C",
# "C-R33-C",
# "R50-C",
# "R33-C",
# ]

all_urls = get_boards(filters)

"""----------------"""
num_chunks = 1
avg_chunk_size = len(all_urls) // num_chunks
remainder = len(all_urls) % num_chunks

chunks = []
start = 0
for i in range(num_chunks):
    end = start + avg_chunk_size + (1 if i < remainder else 0)
    chunks.append(all_urls[start:end])
    start = end
"""----------------"""
# Parameters


def main(boards: list):
    for line in lines:
        for url in boards:  # tqdm(boards):
            strat_actions = load_strat(url, line)

            if strat_actions == "NOLINE":
                continue

            strat, actions = strat_actions
            if len(actions) == 1:
                continue

            max_scores = strat[actions].max(axis=1)
            max_score = max_scores.sum()

            init_action = strat[actions].idxmax(axis=1).value_counts().idxmax()
            strat["action"] = init_action
            init_score = strat[init_action].sum()

            tree = {}

            def append_tree(hand_before, hand):
                keys = [i[0] for i in hand_before if i[1] == 1]
                if len(keys) == 0:
                    tree[hand] = {}
                else:
                    reduce(lambda x, y: x[y], [tree] + keys)[hand] = {}

            def step(
                df: pd.DataFrame,
                hand_before=[],
            ):
                a = df.copy()
                weight = a.shape[0] / strat.shape[0]
                # qw(weight)
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

                hands = [i for i in a.columns if i not in [*actions, "action"] + [f"{j}_gain" for j in actions]]

                def iter_step(col_cnt):
                    result = []
                    for hand in combinations(hands, col_cnt):
                        for action in other_actions:
                            corr_coefficient, p_value = pointbiserialr(a[hand[0]], a[f"{action}_gain"])
                            result.append((hand[0], action, corr_coefficient))

                    return result

                result = iter_step(1)

                if len(result) == 0:
                    return
                result = sorted(result, key=lambda x: abs(x[2]), reverse=True)

                a_result = get_result(a, actions, line, False)
                a_result_sort = sorted([(k, v) for k, v in a_result.items()], key=lambda x: x[1], reverse=True)

                best_cut = result[0]

                bc_1_weight = a[a[best_cut[0]]].shape[0] / a.shape[0] * weight
                bc_1_result = get_result(a[a[best_cut[0]]], actions, line, False)
                bc_1_result_sort = sorted([(k, v) for k, v in bc_1_result.items()], key=lambda x: x[1], reverse=True)

                bc_0_weight = a[~a[best_cut[0]]].shape[0] / a.shape[0] * weight
                bc_0_result = get_result(a[~a[best_cut[0]]], actions, line, False)
                bc_0_result_sort = sorted([(k, v) for k, v in bc_0_result.items()], key=lambda x: x[1], reverse=True)

                print(hand_before, round(weight * 100, 1), a_result_sort)
                print(best_cut[0])
                print(round(bc_1_weight * 100, 1), bc_1_result_sort)
                print(round(bc_0_weight * 100, 1), bc_0_result_sort)
                print("\n")

                append_tree(
                    hand_before,
                    best_cut[0],
                )

                if best_cut[2] > 0:
                    a.loc[a[best_cut[0]], "action"] = best_cut[1]  # ami besc cut filternel a leggyakoribb action\
                else:
                    a.loc[~a[best_cut[0]], "action"] = best_cut[1]

                step(
                    a[a[best_cut[0]]],
                    hand_before + [(best_cut[0], 1)],
                )

                step(
                    a[~a[best_cut[0]]],
                    hand_before + [(best_cut[0], 0)],
                )

            step(strat, [])
            # print(tree)
            # final_score = sum([strat[strat["action"] == action][action].sum() for action in actions])

            def count(prod, c=0):
                for mykey in prod:
                    if isinstance(prod[mykey], dict):
                        # calls repeatedly
                        c = count(prod[mykey], c + 1)
                    else:
                        c += 1
                return c

            # print(
            #     round(init_score / max_score * 100),
            #     round(final_score / max_score * 100),
            #     count(tree),
            # )
            # step(origi_strat, [], True)
            # print(tree)

            def get_freqs(level: dict, a: pd.DataFrame):
                keys = list(level.keys())

                level["rest"] = get_result(
                    a[pd.DataFrame([a[j] == 0 for j in keys]).all(axis=0)],
                    actions,
                    line,
                )

                if len(level[keys[0]]) == 0:
                    level[keys[0]] = get_result(a[a[keys[0]] == 1], actions, line)
                else:
                    get_freqs(level[keys[0]], a[a[keys[0]] == 1])

                if len(keys) == 1:
                    return

                for key in keys[1:]:
                    filter_keys = keys[: keys.index(key) + 1]

                    if len(level[filter_keys[-1]]) == 0:
                        level[filter_keys[-1]] = get_result(
                            a[
                                pd.DataFrame([a[j] == 0 for j in filter_keys[:-1]]).all(axis=0)
                                & (a[filter_keys[-1]] == 1)
                            ],
                            actions,
                            line,
                        )
                    else:
                        get_freqs(
                            level[filter_keys[-1]],
                            a[
                                pd.DataFrame([a[j] == 0 for j in filter_keys[:-1]]).all(axis=0)
                                & (a[filter_keys[-1]] == 1)
                            ],
                        )

            if len(tree) > 0:
                get_freqs(tree, strat)
            # print(tree)
            base_action = get_result(strat, actions, line)

            def build_saved_tree(tree):  # tree without rest
                result = {}
                for i in tree:
                    if "rest" in tree[i]:
                        result[i] = {}
                        result[i]["rest"] = {
                            "action": tree[i]["rest"],
                            "weight": 0,
                        }
                        result[i]["action"] = {}
                        result[i]["weight"] = 0
                        result[i]["sub"] = build_saved_tree({k: v for k, v in tree[i].items() if k != "rest"})
                    else:
                        result[i] = {
                            "action": tree[i],
                            "rest": {},
                            "sub": {},
                            "weight": 0,
                        }
                return result

            if len(tree) > 0:
                final_tree = {
                    "ROOT": {
                        "rest": {"action": tree["rest"], "weight": 0},
                        "sub": {},
                    },
                    "base_action": base_action,
                    "hide": False,
                }
                final_tree["ROOT"]["sub"] = build_saved_tree({k: v for k, v in tree.items() if k != "rest"})
            else:
                final_tree = {
                    "ROOT": {
                        "rest": {},
                        "sub": {},
                    },
                    "base_action": base_action,
                    "hide": False,
                }
            # qw(final_tree)

            filename = f"/Users/barrybaker/Documents/blackcard2/blackcard2_back/app/saved/{url.replace(gto_path,'').replace('.obj','_')}{line}.obj"

            with open(filename, "wb") as f:
                pickle.dump(final_tree, f)


if __name__ == "__main__":
    processes = []
    if len(chunks) <= 9:
        for i in chunks:
            process = multiprocessing.Process(target=main, args=(i,))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()
