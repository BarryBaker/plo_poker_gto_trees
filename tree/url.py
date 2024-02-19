import numpy as np
import pandas as pd

from icecream import ic as qw

from omaha._cards import Board

from .load_strat import get_board_from_link, get_pot_from_link
from ._utils import split_lines_tostreets


class Url:
    def __init__(self, url: str) -> None:
        self.url = url

    @property
    def board(self):
        return Board(get_board_from_link(self.url))

    @property
    def pot(self):
        return get_pot_from_link(self.url)


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
