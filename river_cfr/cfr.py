import glob
import random
import pandas as pd
import numpy as np
from tqdm import tqdm
import multiprocessing
from multiprocessing import shared_memory, Lock
import pprint

# from icecream import ic as qw
import pickle

from .omaha.Equity import Card
from .omaha.Equity import Evaluator
from .omaha.Equity import Deck

from .ahk.ahk import Ahk
from .ahk.board import RiverBoard
from .ahk.actions import Tree
from .ahk.static import cardValues, suitValues

from .tree._tree import build_tree
from .tree.tree._utils import convert_action_name


# from ahk.browse_data import find_ahks
from .utils.actions_copy import actions, terminals, payoff
from .utils.utils import river_cat

import time

# import logging

# obj3 = "/Users/barrybaker/Documents/fromAHK/objs3/"

# [
#         (
#             "/Users/barrybaker/Documents/fromAHK/data/100_BTN_BB_SRP/ahks/PLO500_100_6_BTN_BB_SRP_AsKd5c8c_BTNvsBB_C-C-C-C-C.ahk",
#             "8h",
#         ),

#     ]


def compute_river(rivers):

    def main(ahk, river, iterations):

        def normalize(strategy: np.array) -> np.array:
            """Normalize a strategy. If there are no positive regrets,
            use a uniform random strategy"""
            num_actions = len(strategy)
            if sum(strategy) > 0:
                strategy /= sum(strategy)
            else:
                strategy = np.array([1.0 / num_actions] * num_actions)
            return strategy

        start_time = time.time()
        # situ = "100_BTN_BB_SRP"
        # ahk = f"/Users/barrybaker/Documents/fromAHK/data/{situ}/ahks/PLO500_100_6_BTN_BB_SRP_AsKd5c8c_BTNvsBB_C-C-C-C-C.ahk"

        ahk = Ahk(ahk)

        # river = "4h"
        ranges = ahk.ranges
        # print(ranges)

        # -------------------------------
        # iterations = 2000000  # 3_000_000
        ranges = ahk.ranges_discarded(river)

        board = ahk.board + [river]
        eval_board = [Card.new(i) for i in board]

        riverboard = RiverBoard(board)
        flushes = list(
            set(
                riverboard.flush_draw
                + riverboard.flush
                # if riverboard.flush
                # else []
            )
        )
        # print(flushes)
        # print(ranges)
        rng = np.random.default_rng()
        evaluator = Evaluator()

        # cards1 = {}
        # size = {}
        picked_rows = {}
        # picked_cards = {}
        values = {}
        combo_np = {}
        picked_combo_np = {}

        for i in ranges:
            # print(1)
            ranges[i]["value"] = ranges[i].index.map(
                lambda x: evaluator._seven(
                    eval_board
                    + [Card.new(i) for i in [x[2 * i] + x[2 * i + 1] for i in range(4)]]
                )
            )
            # print(1.5)
            ranges[i]["ranks"] = ranges[i].index.map(lambda x: x[0] + x[2] + x[4] + x[6])
            for n, s in enumerate(flushes):
                ranges[i][f"suit_{n}"] = ranges[i].index.map(
                    lambda x: "".join(
                        np.where(np.array([x[1], x[3], x[5], x[7]]) == s)[0].astype(str)
                    )
                )
            # print(2)
            # ranges[i]["combo_np"] = ranges[i].index.map(lambda x: cardValues[x[0]]*4 + x[2] + x[4] + x[6])
            # for index, x in ranges[i].iterrows():
            #     print(x.name)
            combo_np[i] = np.array(
                [
                    [
                        cardValues[x.name[j]] * 4 + suitValues[x.name[j + 1]]
                        for j in [0, 2, 4, 6]
                    ]
                    for index, x in ranges[i].iterrows()
                ]
            )
            # print(3)
            if len(flushes) >= 2:
                ranges[i]["cat"] = (
                    ranges[i]["ranks"] + ranges[i]["suit_0"] + "_" + ranges[i]["suit_1"]
                )
            elif len(flushes) == 1:
                ranges[i]["cat"] = ranges[i]["ranks"] + ranges[i]["suit_0"]
            else:
                ranges[i]["cat"] = ranges[i]["ranks"]
            ranges[i]["cat_int"] = ranges[i]["cat"].astype("category").cat.codes

            # cards1[i] = ranges[i].index
            # size[i] = ranges[i].shape[0]
            picked_rows[i] = rng.integers(0, ranges[i].shape[0] - 1, iterations)

            # print(ranges[i].iloc[picked_rows[i]])
            picked_combo_np[i] = combo_np[i][picked_rows[i]]
            # picked_cards[i] = [cards1[i][n] for n in picked_rows[i]]
        # print(4)
        cnp = [i for i in picked_combo_np.values()]
        # print(cnp[0].shape, cnp[1].shape)
        combo_np = np.concatenate((cnp[0], cnp[1]), axis=1)

        sorted_arr = np.sort(combo_np, axis=1)
        to_delete = np.all(sorted_arr[:, :-1] != sorted_arr[:, 1:], axis=1)
        # print(5)
        # print(ranges, picked_rows, to_delete)
        cats = {}
        for i in ranges:
            picked_rows[i] = picked_rows[i][to_delete]

            picked_ranges = ranges[i].iloc[picked_rows[i]]
            values[i] = picked_ranges["value"].values
            cats[i] = picked_ranges["cat_int"].values

            # values[i] = ranges[i]["value"].values[~to_delete]
            # cats[i] = ranges[i]["cat_int"].values[~to_delete]
            # values[i] = [ranges[i]["value"].iloc[j] for j in picked_rows[i]]
            # cats[i] = [ranges[i]["cat_int"].iloc[j] for j in picked_rows[i]]
            # picked_cards[i] = [cards1[i][n] for n in picked_rows[i]]
        # print(6)
        # print(ranges)
        players = ahk.players
        players.reverse()
        iterations = picked_rows[players[0]].size

        # for i in ranges:
        #     print(values[i][:10], len(values[i]), cats[i][:10], len(cats[i]))
        # print("finish 1", "  ", (time.time() - start_time))

        # cards = [[ranges[i]["cat_int"].iloc[j] for j in picked_rows[i]] for i in players]

        tree = Tree(
            # {
            #     "": ["C", "A"],
            #     "C-A": ["F", "C"],
            #     "C": ["C", "A"],
            #     "A": ["F", "C"],
            # },
            {
                "": ["C", "R100"],
                "C-R100": ["F", "C", "A"],
                "C": ["C", "R100"],
                "R100": ["F", "C", "A"],
                "R100-A": ["F", "C"],
                "C-R100-A": ["F", "C"],
            },
            # {
            #     "": ["C", "R75"],
            #     "C-R75": ["F", "C", "R75"],
            #     "C": ["C", "R75"],
            #     "R75": ["F", "C", "R75"],
            #     "R75-R75": ["F", "C", "A"],
            #     "C-R75-R75": ["F", "C", "A"],
            #     "C-R75-R75-A": ["F", "C"],
            #     "R75-R75-A": ["F", "C"],
            # },
            # {
            #     "": ["C", "R75"],
            #     "C-R75": ["F", "C", "R75"],
            #     "C": ["C", "R75"],
            #     "R75": ["F", "C", "R75"],
            #     "R75-R75": ["F", "C", "A"],
            #     "C-R75-R75": ["F", "C", "A"],
            #     "C-R75-R75-A": ["F", "C"],
            #     "R75-R75-A": ["F", "C"],
            # },
            ahk.spr,
        )
        actions = tree.actions

        terminals = tree.terminals
        payoff = tree.payoff
        # for i in payoff:
        #     print(i, payoff[i])

        original_nodes = {}
        for node in actions:
            playerId = len(node.split("-")) % 2 if len(node) > 0 else 0

            player = players[playerId]

            original_nodes[node] = np.zeros(
                (
                    ranges[player]["cat_int"].max() + 1,
                    2,
                    len(actions[node]),
                ),
            )

        # print(original_nodes)

        def cfr(iter, history, reach_probabilities, active_player):
            opponent = (active_player + 1) % 2
            if history in terminals:
                return (
                    payoff[history][2]
                    if values[players[0]][iter] == values[players[1]][iter]
                    else payoff[history][
                        1 if values[players[0]][iter] > values[players[1]][iter] else 0
                    ]
                )
            cumulative_regrets = original_nodes[history][
                cats[players[active_player]][iter]
            ][0]
            cumulative_regrets = np.maximum(0, cumulative_regrets)
            strategy = normalize(cumulative_regrets)

            counterfactual_values = [None] * len(actions[history])

            for ix, action in enumerate(actions[history]):
                action_probability = strategy[ix]

                new_reach_probabilities = reach_probabilities.copy()
                new_reach_probabilities[active_player] *= action_probability

                counterfactual_values[ix] = cfr(
                    iter,
                    f"{history}-{action}".strip("-"),
                    new_reach_probabilities,
                    opponent,
                )

            node_values = strategy.dot(counterfactual_values)

            if reach_probabilities[opponent] > 0:
                regrets = np.zeros(len(actions[history]))
                for ix, action in enumerate(actions[history]):
                    cf_reach_prob = reach_probabilities[opponent]

                    regret = (
                        counterfactual_values[ix][active_player]
                        - node_values[active_player]
                    )

                    regrets[ix] = cf_reach_prob * regret

                original_nodes[history][cats[players[active_player]][iter]][0] = (
                    original_nodes[history][cats[players[active_player]][iter]][0]
                    + regrets
                )

                cumulative_regrets = np.maximum(
                    0,
                    original_nodes[history][cats[players[active_player]][iter]][0],
                )
                strategy = normalize(cumulative_regrets)
                if iter > iterations / 20:
                    original_nodes[history][cats[players[active_player]][iter]][1] = (
                        original_nodes[history][cats[players[active_player]][iter]][1]
                        + reach_probabilities[opponent] * strategy
                    )

            return node_values

        def train():
            for i in tqdm(range(iterations)):
                # start_time = time.time()
                cfr(i, "", np.ones(2), 0)
                # print("finsih", "  ", (time.time() - start_time))

        train()
        result = []
        strat_results = []
        # print(board)
        for i in actions:
            if i in ["", "C"]:

                final_line = f"{ahk.line.origi_line}-{i}".strip("-")

                playerId = len(i.split("-")) % 2 if len(i) > 0 else 0

                player = players[playerId]

                rowsnr = ranges[player].shape[0]

                result_sample = np.zeros((rowsnr, len(actions[i])))
                for j in range(rowsnr):
                    result_sample[j] = normalize(
                        original_nodes[i][ranges[player].iloc[j, :]["cat_int"]][1]
                    )

                strat = ranges[player].copy()

                for nr, action in enumerate(actions[i]):
                    strat[action] = result_sample[:, nr] * strat["weight"]  # / 100
                # print(strat)
                strat.drop(
                    strat.columns.difference(actions[i]),
                    axis=1,
                    inplace=True,
                )
                # print(strat, actions[i])
                # print(i, "-----")
                # print("elso", strat_results)
                # strat_results.append(strat.copy())
                # print("utana", strat_results)
                strat_results.append(
                    {"strat": strat.copy(), "line": final_line, "board": "".join(board)}
                )
                # print(strat_results)
                # print("----------------")
                # strat = strat.applymap(lambda x: int(x * 100))
                # print(i, strat.sample(20))
                # sumactions = np.sum(strat.values)
                # for action in actions[i]:
                #     print(
                #         action,
                #         round(np.sum(strat[action]) * 100 / sumactions, 2),
                #     )
                # pprint.pprint(build_tree(strat, "".join(board), final_line))
                # result[final_line] = strat

                result.append(
                    {
                        "tree": build_tree(strat, "".join(board), final_line),
                        "board": "".join(board),
                        "layer": "river",
                        "line": i if i != "" else "NO",
                        "actions": [convert_action_name(j, "C-C") for j in actions[i]],
                    }
                )
        # print(strat_results)
        return result, strat_results
        # print(result)
        # with open(obj3 + obj_name, "wb") as f:
        #     pickle.dump(result, f)
        # strat["action"] = strat.idxmax(axis=1)

        # print(strat.sample(20))
        # for action in actions[i]:
        #     print(
        #         action,
        #         round(np.sum(strat[action]) / rowsnr, 2),
        #     )

        # print("\n-----------------------------------------------\n")

    # if __name__ == "__main__":
    # print("aaaaa")
    # processes = []
    iter = 2_000_000
    return main(rivers[0], rivers[1], iter)
    # for i in rivers:
    #     process = multiprocessing.Process(target=main, args=(i[0], i[1], iter))
    #     process.start()
    #     processes.append(process)

    # for process in processes:
    #     process.join()
