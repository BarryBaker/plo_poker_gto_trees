import numpy as np
import pandas as pd

from ._utils import split_lines_tostreets


class Line:
    def __init__(self, line: str, mw: bool = False) -> None:
        self.line = line.split("-")
        self.mw = mw

    @property
    def streets(self):
        return split_lines_tostreets(self.line)

    @property
    def is_attack(self):
        return (
            self.line[0] == ""
            or (not self.mw and self.line[-1] == "C")
            or (self.mw and self.line[-1] == "C" and len(self.line) == 1)
            or (
                self.mw
                and self.line[-1] == "C"
                and self.line[-2] == "C"
                and len(self.line) > 1
            )
        )
