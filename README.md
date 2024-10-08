# plo_poker_gto_trees

AI Tree for Pot Limit Omaha GTO Solutions

Overview

This project is designed to take GTO (Game Theory Optimal) solved solutions for Pot Limit Omaha (PLO) poker and build decision trees in JSON format. These trees offer a human-readable format that simplifies the complex data from solvers, allowing you to observe general strategic rules such as:

    •	Always bet a set.
    •	Bet good straight draws, check bad straight draws.

{"stack": "100",
"poss": "BTN_BB",
"pot": "SRP",
"board": "AsKd5cAh",
"line": "C-C",
"tree": {"ROOT": [[98, 2], 
 {"FULL": [[78, 22], {"LP": [[21, 79], {"TRIPS1": [[39, 61], {"RR": [[85, 15], []], "GS": [[57, 43], []], "FULL1": [[70, 30], []]}]}], "FULL1": [[48, 52], {"TRIPS1": [[73, 27], []]}], "RR": [[41, 59], {"LRR": [[66, 34], []]}]}], "TRIPS": [[39, 61], {"HRR": [[64, 36], []], "SD": [[41, 59], {"TRIPS1": [[49, 51], {"WR": [[83, 17], []]}], "RR": [[52, 48], []]}]}], "BOP": [[72, 28], {"TP": [[99, 1], {"LP": [[89, 11], []], "Q": [[30, 70], []]}], "HRR": [[83, 17], []], "SD": [[11, 89], []], "RR": [[19, 81], []], "Q": [[8, 92], []]}], "RR": [[96, 4], {"LRR": [[73, 27], {"SD": [[8, 92], []], "DRR": [[5, 95], {"HRR": [[53, 47], []]}]}]}], "SD": [[69, 31], {"WR": [[1, 99], []], "OESD": [[6, 94], []], "Q": [[0, 100], []]}], "Q": [[2, 98], []]}], "base_action": [70, 30]}, "layer": "turn", "hero": "BB", "actions": ["CHECK", "RAISE75"]}

combo,weight
QcQs3s2s,100
QhQs3s2s,100
Ac3s2c2s,100
Ah3s2h2s,100
6c5c3s2s,100
6h5h3s2s,100

combo,weight
KcKs3s2s,100
KhKs3s2s,100
Jc3s2c2s,3
Jh3s2h2s,3
Kc3s2c2s,100
Kh3s2h2s,100
