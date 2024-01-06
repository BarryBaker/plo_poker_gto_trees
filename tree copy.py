import pandas as pd
import numpy as np
import pickle
import multiprocessing

from collections import Counter
from functools import reduce

from itertools import combinations
from time import time
from icecream import ic as qw
from tqdm import tqdm

from load_strat import load_strat, get_boards


gto_path = "/Users/barrybaker/Documents/fromAHK/objs3/"


situation = {
    "stack": "100",
    "poss": ["BTN", "BB"],
    "pot": "SRP",
}
lines = ["C-R75-C-C-R100"]

situation["poss"] = "_".join(situation["poss"])

all_boards = get_boards(situation)


"""----------------"""
num_chunks = 1
avg_chunk_size = len(all_boards) // num_chunks
remainder = len(all_boards) % num_chunks

chunks = []
start = 0
for i in range(num_chunks):
    end = start + avg_chunk_size + (1 if i < remainder else 0)
    chunks.append(all_boards[start:end])
    start = end
"""----------------"""
min_loss_decrease = 0.2


def main(boards: list):
    # board = None  # "Js8d2s" + turn
    for line in lines:
        for board in tqdm(boards):
            strat_actions = load_strat(situation, board, line)
            if strat_actions == "NOLINE":
                continue
            strat, actions = strat_actions
            if len(actions) == 1:
                continue
            # if len(actions) > 2:

            # def convert_action_name(a):
            #     if a == "C":
            #         if line[-1] == "C":
            #             return "CHECK"
            #         return "CALL"
            #     if a[0] == "R":
            #         return f"RAISE{a[1:]}"
            #     return {"F": "FOLD", "C": "CALL"}[a]

            max_score = strat.apply(
                lambda row: sorted([row[i] for i in actions])[-2]
                - sorted([row[i] for i in actions])[-1],
                axis=1,
            ).sum()

            # hand_count = strat.shape[0]

            init_action = (
                strat[actions].idxmax(axis=1).value_counts().idxmax()
            )
            strat["action"] = init_action

            qw(board, strat.iloc[:, :7].sample(20))
            # init_score = round(
            #     strat.apply(
            #         lambda row: sorted(
            #             [row[i] for i in actions if i != row["action"]]
            #         )[-1]
            #         - row[row["action"]],
            #         axis=1,
            #     ).sum()
            #     / max_score
            #     * 100,
            #     2,
            # )

            tree = {}

            def append_tree(hand_before, hand):
                keys = [i[0] for i in hand_before if i[1] == 1]
                if len(keys) == 0:
                    tree[hand] = {}
                else:
                    reduce(lambda x, y: x[y], [tree] + keys)[hand] = {}

            def step(df: pd.DataFrame, hand_before=[]):
                a = df.copy()

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

                # if len([i for i in a.columns if i not in actions]) == 0:
                #     return
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
                # qw(hand_before)
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

                if len(result) == 0:
                    return
                result = sorted(result, key=lambda x: x[2], reverse=True)
                # qw(result[:5])
                best_cut = result[0]
                loss_decrease = -round(
                    2 * best_cut[2] / max_score * 100, 3
                )

                # qw(best_cut, loss_decrease)

                if loss_decrease >= min_loss_decrease:
                    # qw("  " * sum([i[1] for i in hand_before]) + best_cut[0])
                    append_tree(
                        hand_before,
                        best_cut[0],
                        # "",  # [i for i in actions if i != a.action.iloc[0]][0],
                    )

                    a.loc[a[best_cut[0]] == best_cut[1], "action"] = a[
                        "action"
                    ].apply(lambda x: [i for i in actions if i != x][0])
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
                        strat.loc[
                            strat[best_cut[0]] == best_cut[1], "action"
                        ] = strat["action"].apply(
                            lambda x: [i for i in actions if i != x][0]
                        )

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
                            filtered = a[
                                (a[hand[0]] == tf[0])
                                & (a[hand[1]] == tf[1])
                            ]

                            if filtered.shape[0] > 0:
                                loss = sum(filtered["loss"])
                                if loss > 0:
                                    result.append(
                                        (hand, tf, loss)
                                    )  # / a.shape[0])

                    result = sorted(
                        result, key=lambda x: x[2], reverse=True
                    )
                    result = [
                        i
                        for i in result
                        if round(2 * i[2] / (loss - max_score) * 100, 3)
                        > 1
                    ]
                    if len(result) == 0:
                        return
                        """--------------------------------"""
                        result = []
                        for hand in combinations(
                            [
                                "2",
                                "3",
                                "4",
                                "5",
                                "6",
                                "7",
                                "8",
                                "9",
                                "T",
                                "J",
                                "K",
                                "A",
                            ],
                            3,
                        ):
                            for tf in [
                                # (0, 0, 0),
                                # (0, 1, 0),
                                # (1, 0, 0),
                                # (1, 1, 0),
                                # (0, 0, 1),
                                # (0, 1, 1),
                                # (1, 0, 1),
                                (1, 1, 1),
                            ]:
                                filtered = a[
                                    (a[hand[0]] == tf[0])
                                    & (a[hand[1]] == tf[1])
                                    & (a[hand[2]] == tf[2])
                                ]

                                if filtered.shape[0] > 0:
                                    loss = sum(filtered["loss"])
                                    if loss > 0:
                                        result.append(
                                            (hand, tf, loss)
                                        )  # / a.shape[0])

                        result = sorted(
                            result, key=lambda x: x[2], reverse=True
                        )
                        result = [
                            i
                            for i in result
                            if round(
                                2 * i[2] / (loss - max_score) * 100, 3
                            )
                            > 1
                        ]
                        if len(result) == 0:
                            return
                        best_cut = result[0]
                        loss_decrease = round(
                            2 * best_cut[2] / (loss - max_score) * 100, 2
                        )

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
                        """--------------------------------"""
                    best_cut = result[0]
                    loss_decrease = round(
                        2 * best_cut[2] / (loss - max_score) * 100, 2
                    )
                    if loss_decrease < min_loss_decrease:
                        return
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
                return {
                    convert_action_name(k): v for k, v in result.items()
                }

            def get_freqs(level: dict, a: pd.DataFrame):
                keys = list(level.keys())

                # if len(keys) == 0:

                #     level = get_result(a)

                #     return

                # Rest.  itt van vmi bug
                # try:
                level["rest"] = get_result(
                    a[pd.DataFrame([a[j] == 0 for j in keys]).all(axis=0)]
                )
                # except:
                #     qw(original_tree)
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
            # qw(tree)

            base_action = get_result(strat)

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
                            {
                                k: v
                                for k, v in tree[i].items()
                                if k != "rest"
                            }
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

            filename = f"/Users/barrybaker/Documents/blackcard2/blackcard2_back/app/saved/{'_'.join(list(situation.values()))}_{board}_{line}.obj"

            # with open(filename, "wb") as f:
            #     pickle.dump(final_tree, f)


if __name__ == "__main__":
    processes = []
    if len(chunks) <= 9:
        for i in chunks:
            process = multiprocessing.Process(target=main, args=(i[:27],))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()
