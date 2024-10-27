# AI Tree for Pot Limit Omaha GTO Solutions

Overview

This project processes GTO (Game Theory Optimal) solved solutions for Pot Limit Omaha (PLO) poker and generates decision trees in JSON format. The trees provide human-readable insights from the solver data, making it easier to observe general rules, such as:

    •	Always bet a set.
    •	Bet good straight draws, check bad straight draws.

The decision trees are designed to be concise, typically around 40-60 lines, while retaining key strategic insights. The goal is to present GTO solutions in a more humanly processable form without losing much of the solver’s depth.

Input

The input is a CSV file, commonly generated from solvers, with the following format:

combo,weight
KcKs3s2s,100
KhKs3s2s,100
Jc3s2c2s,3
Jh3s2h2s,3
Kc3s2c2s,100
Kh3s2h2s,100

Each row represents a possible hand (card combo) and the associated weight or frequency that a player should take an action with that hand.

Features

    •	Decision Tree Generation: Converts raw solver output into a simplified decision tree format.
    •	Compact Representation: The algorithm optimizes for the smallest possible tree that still represents important GTO strategies.
    •	Human-Readable JSON: Outputs a nested JSON structure that can be used for visualization or further analysis.
    •	Strategic Insights: Offers a way to extract general rules from solver data, like “always bet a set.”

Installation

    1.	Clone the repository:
    git clone https://github.com/BarryBaker/AI_tree.git
    cd AI_tree

    2. Set up the virtual environment and install dependencies:
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

Usage

To run the program, simply call main.py with CSV filenames:

python main.py PLO500_100_6_BTN_BB_SRP_Ks7d5d_C_BTN_CHECK.csv PLO500_100_6_BTN_BB_SRP_Ks7d5d_C_BTN_RAISE75.csv

The solved folder contains sample CSV files, which you can use directly. If no files are specified, default sample files from the solved folder will be used.

Here’s an example of the formatted output:
{
"ROOT": {
"TRIPS": {
"2PT": {
"action": {"CHECK": 45, "RAISE75": 55},
"weight": "5.98%"
},
"LP": {
"action": {"CHECK": 24, "RAISE75": 76},
"weight": "18.21%"
},
"NFD": {
"action": {"CHECK": 50, "RAISE75": 50},
"weight": "1.03%"
},
"action": {"CHECK": 16, "RAISE75": 84},
"weight": "57.39%"
}
}
}
