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
import warnings

warnings.filterwarnings("error")
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
min_gain = 1  # %
min_gain_doubles_multiplicatow = 2  # how stronger doubles shoudl find
split_strength_weights_2 = 10  # 10
split_strength_weights_3 = 20  # 20


def main(boards: list):
    for line in lines:
        for url in tqdm(boards):
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
            # qw(strat.loc[strat["TRIPS"], actions])

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
                filtresult = get_result(a, actions, line, False)
                # qw(hand_before, round(weight * 100, 2), filtresult)
                a.drop(
                    [
                        c
                        for c in [
                            i
                            for i in a.columns
                            if i not in actions + ["action"]
                        ]
                        if (np.all(a[c]) or np.all(~a[c]))
                    ],
                    axis=1,
                    inplace=True,
                )

                # current_action = np.unique(a["action"])
                # if len(current_action) > 1:
                #     raise Exception("Multiple action options in iterate step")
                # current_action = current_action[0]
                # other_actions = [j for j in actions if j != current_action]

                # for i in other_actions:
                #     a[f"{i}_gain"] = a[i] - a[current_action]

                # print(a.iloc[:, [0, 1, 2, 3, 4, -3, -2, -1]].sample(20))

                hands = [
                    i
                    for i in a.columns
                    if i
                    not in [*actions, "action"] + [f"{j}_gain" for j in actions]
                ]

                def iter_step(col_cnt):
                    result = []
                    for hand in combinations(hands, col_cnt):
                        for action in actions:
                            # print(hand, a[hand[0]])
                            try:
                                corr_coefficient, p_value = pointbiserialr(
                                    a[hand[0]], a[action]
                                )
                            except:
                                continue
                            result.append((hand[0], action, corr_coefficient))

                        # scores[hand] = abs(true_values - false_values)

                        # if filtered.shape[0] > 0:
                        #     filtresult = get_result(
                        #         filtered, actions, line, False
                        #     )
                        #     largest_action = max(filtresult, key=filtresult.get)

                        #     largest_value = filtresult[largest_action]

                        #     for action in other_actions:
                        #         result.append(
                        #             (
                        #                 hand,
                        #                 tf,
                        #                 sum(filtered[f"{action}_gain"]),
                        #                 action,
                        #                 largest_action,
                        #                 largest_value,
                        #                 filtresult,
                        #                 round(
                        #                     filtered.shape[0]
                        #                     / strat.shape[0]
                        #                     * 100
                        #                 ),
                        #             )
                        #         )
                    return result

                result = iter_step(1)

                if len(result) == 0:
                    return
                result = sorted(result, key=lambda x: abs(x[2]), reverse=True)

                best_cut = result[0]
                # score_gain = best_cut[2]

                # qw(
                #     best_cut[0],
                #     round(a[a[best_cut[0]]].shape[0] * 100 / a.shape[0]),
                #     get_result(a[a[best_cut[0]]], actions, line, False),
                #     get_result(a[~a[best_cut[0]]], actions, line, False),
                #     "\n",
                # )
                largest_actions1 = max(
                    get_result(a[a[best_cut[0]]], actions, line, False),
                    key=get_result(a[a[best_cut[0]]], actions, line, False).get,
                )
                largest_actions2 = max(
                    get_result(a[~a[best_cut[0]]], actions, line, False),
                    key=get_result(
                        a[~a[best_cut[0]]], actions, line, False
                    ).get,
                )
                # qw(largest_actions1, largest_actions2)

                if not (weight < 1 and largest_actions1 == largest_actions2):
                    append_tree(
                        hand_before,
                        best_cut[0],
                    )

                    # a.loc[a[best_cut[0]], "action"] = best_cut[
                    #     1
                    # ]  # ami besc cut filternel a leggyakoribb action

                    # if len(hand_before) > 0:
                    #     strat.loc[
                    #         (strat[best_cut[0][0]] == best_cut[1])
                    #         & pd.DataFrame(
                    #             [strat[i[0]] == i[1] for i in hand_before]
                    #         ).all(axis=0),
                    #         "action",
                    #     ] = best_cut[4]
                    # else:
                    #     strat.loc[
                    #         strat[best_cut[0][0]] == best_cut[1], "action"
                    #     ] = best_cut[4]

                    step(
                        a[a[best_cut[0]]],
                        hand_before + [(best_cut[0], 1)],
                    )

                    step(
                        a[~a[best_cut[0]]],
                        hand_before + [(best_cut[0], 0)],
                    )
                # if bestcut itself has mostly diferent action than current
                elif True:
                    return

                elif best_cut[4] != current_action and best_cut[5] > 60:
                    append_tree(
                        hand_before,
                        best_cut[0],
                    )

                    a.loc[a[best_cut[0]] == best_cut[1], "action"] = best_cut[4]

                    if len(hand_before) > 0:
                        strat.loc[
                            (strat[best_cut[0]] == best_cut[1])
                            & pd.DataFrame(
                                [strat[i[0]] == i[1] for i in hand_before]
                            ).all(axis=0),
                            "action",
                        ] = best_cut[4]
                    else:
                        strat.loc[
                            strat[best_cut[0]] == best_cut[1], "action"
                        ] = best_cut[4]

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

                    two_largest = [
                        v for k, v in get_result(a, actions, line).items()
                    ]
                    second_largest = sorted(two_largest)[-2]
                    weight = 100 * a.shape[0] / strat.shape[0]

                    if second_largest / 100 * weight < split_strength_weights_2:
                        return

                    if len(result) == 0:
                        if (
                            second_largest / 100 * weight
                            < split_strength_weights_3
                        ):
                            return

                        if len(result) == 0:
                            return
                        result = sorted(
                            result, key=lambda x: x[2], reverse=True
                        )

                        best_cut = result[0]
                        score_gain = best_cut[2]

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

                    result = sorted(result, key=lambda x: x[2], reverse=True)

                    best_cut = result[0]
                    score_gain = best_cut[2]

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

            # origi_strat = strat.copy()
            step(strat, [])
            # for i in tree:
            #     print(i, "\n", tree[i], "\n")
            # print(tree)
            final_score = sum(
                [
                    strat[strat["action"] == action][action].sum()
                    for action in actions
                ]
            )

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

                # if len(keys) == 0:

                #     level = get_result(a,actions,line)

                #     return

                # Rest.  itt van vmi bug
                # try:
                level["rest"] = get_result(
                    a[pd.DataFrame([a[j] == 0 for j in keys]).all(axis=0)],
                    actions,
                    line,
                )
                # except:
                #     qw(original_tree)
                if len(level[keys[0]]) == 0:
                    level[keys[0]] = get_result(
                        a[a[keys[0]] == 1], actions, line
                    )
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
                            ],
                            actions,
                            line,
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

            # def print_tree(tree, indent):
            #     for key in tree:
            #         if key == "rest" and indent > 0:
            #             continue
            #         if list(tree[key].keys())[0] in actions:
            #             print(
            #                 " ".join([""] * indent * 4),
            #                 key,
            #                 [j for j in tree[key].values()],
            #             )

            #         else:
            #             print(
            #                 " ".join([""] * indent * 4),
            #                 key,
            #                 [j for j in tree[key]["rest"].values()],
            #             )
            #             print_tree(tree[key], indent + 1)
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
                        result[i]["sub"] = build_saved_tree(
                            {k: v for k, v in tree[i].items() if k != "rest"}
                        )
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
                final_tree["ROOT"]["sub"] = build_saved_tree(
                    {k: v for k, v in tree.items() if k != "rest"}
                )
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
