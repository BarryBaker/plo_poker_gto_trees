class Line:
    def __init__(self, line) -> None:
        self._line = line.split("-")

    @property
    def line(self):
        if self._line[-1] == "C" and self._line[-2] == "C" and len(self._line) > 2:
            return self._line[:-1]

        return self._line

    @property
    def origi_line(self):
        return "-".join(self.line)

    @property
    def streets(self):
        if self.line[0] == "C":
            otherC = [k for k, n in enumerate(self.line) if n == "C"][1]
        else:
            otherC = [k for k, n in enumerate(self.line) if n == "C"][0]
        flopLine = self.line[: otherC + 1]
        turnLine = self.line[otherC + 1 :]
        return flopLine, turnLine

    def __repr__(self):
        return f"|| {(' - '.join([' '.join(i) for i in self.streets]))} ||"

    @property
    def pot(self):
        pot = 1
        for street in self.streets:
            if len(set(street)) == 1:
                continue
            for step, action in enumerate(street):
                before = street[step - 1] if step > 0 else None
                beforebefore = street[step - 2] if step > 1 else None
                size = None
                if action not in ["C", "MR"]:
                    size = int(action[1:])
                if action == "MR":
                    size = int(before[1:])

                if before == "C" or before is None:
                    if action != "C":
                        pot = pot * (1 + (size / 100))

                else:
                    before_size = (
                        int(before[1:]) if before != "MR" else int(beforebefore[1:])
                    )
                    # First, call no matter what
                    pot_before = pot / (1 + (before_size / 100))

                    pot = pot_before + 2 * pot_before * (before_size / 100)
                    # Then might raise
                    if action != "C":
                        pot = pot * (1 + (size / 100))
        return pot


# print(Line("C-R50-C-C-R33-C").pot)
