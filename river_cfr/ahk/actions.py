class Tree:
    def __init__(self, actions: dict, spr: float):
        self.actions = actions
        self.spr = spr

    @property
    def terminals(self):
        result = []

        def iter_history(key: str):
            for i in self.actions[key]:
                next = f"{key}-{i}".strip("-")
                if next in self.actions:
                    iter_history(next)
                else:
                    if next not in result:
                        result.append(next)

        for key in self.actions:
            iter_history(key)
        result.sort()
        return result

    def winner(self, line: str, cards: tuple) -> int:
        line = line.split("-")

        if "F" in line:
            return (line.index("F") % 2 + 1) % 2
        if cards[0] != cards[1]:
            return 1 if cards[0] < cards[1] else 0
        return 0.5

    def pot(self, line):
        line = line.split("-")

        if line[-1] == "C" and line[-2] == "A":
            return 2 * self.spr + 1

        pot = 1

        for step, action in enumerate(line):
            if action == "F":
                continue
            before = line[step - 1] if step > 0 else None
            after = line[step + 1] if step < len(line) - 1 else None
            size = int(action[1:]) if action[0] == "R" else None

            if after == "F":
                action = "C"

            if before == "C" or before is None:
                if action != "C":
                    pot = pot * (1 + (size / 100))

            else:
                before_size = int(before[1:])
                # First, call no matter what
                pot_before = pot / (1 + (before_size / 100))
                pot = pot_before + 2 * pot_before * (before_size / 100)
                # Then might raise
                if action != "C":
                    pot = pot * (1 + (size / 100))
        return pot

    @property
    def payoff(self):
        result = {}
        for i in self.terminals:
            win_amount = (self.pot(i) - 1) / 2 + 1
            loose_amount = (self.pot(i) - 1) / 2
            if "F" in i:
                winner = self.winner(i, ())
                result[i] = [
                    (
                        [win_amount, -loose_amount]
                        if winner == 0
                        else [-loose_amount, win_amount]
                    ),
                    (
                        [win_amount, -loose_amount]
                        if winner == 0
                        else [-loose_amount, win_amount]
                    ),
                    [0.5, 0.5],  # split pot
                ]

            else:
                result[i] = [
                    [win_amount, -loose_amount],
                    [-loose_amount, win_amount],
                    [0.5, 0.5],  # split pot
                ]
        return result


if __name__ == "__main__":

    barrel = Tree(
        {
            "": ["C", "R100"],
            "C-R100": ["F", "C", "A"],
            "C": ["C", "R100"],
            "R100": ["F", "C", "A"],
            "R100-A": ["F", "C"],
            "C-R100-A": ["F", "C"],
        },
        1.566,
    )
    ip(barrel.payoff)
