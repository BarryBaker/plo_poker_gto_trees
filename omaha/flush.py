# from tree.cards import Cards
import numpy as np

from itertools import combinations

from ._cards import Board, Cards
from ._static import card_values_inv
from ._utils import f1, f2, f1_card


def bdfd(cards: Cards, board: Board):
    suits = cards.suits
    bdfd = board.bdfd

    if len(bdfd) == 0:
        return cards.empty

    return np.any(
        [f2(suits, suit) for suit in bdfd],
        axis=0,
    )


def bdfd_2(cards: Cards, board: Board):
    suits = cards.suits
    bdfd = board.bdfd

    if len(bdfd) < 2:
        return cards.empty

    return np.any(
        [
            np.all([f2(suits, s) for s in suit], axis=0)
            for suit in combinations(bdfd, 2)
        ],
        axis=0,
    )


def fd(cards: Cards, board: Board):
    suits = cards.suits
    fd = board.fd

    if len(fd) == 0:
        return cards.empty

    return np.any(
        [f2(suits, card) for card in fd],
        axis=0,
    )


def dfd(cards: Cards, board: Board):
    suits = cards.suits
    fd = board.fd
    if len(board.cards) != 4 or len(fd) < 0:
        return cards.empty

    return np.all(
        [f2(suits, card) for card in fd],
        axis=0,
    )


def fd_h(level):
    def fld(cards: Cards, board: Board):
        suits = cards.suits
        fd = board.fd

        if len(fd) == 0:
            return cards.empty

        remaining = {
            suit: [
                c
                for c in card_values_inv
                if c not in board.cards[board.cards[:, 1] == suit][:, 0]
            ]
            for suit in fd
        }

        return np.any(
            [
                np.all(
                    [
                        np.any(
                            [
                                f1_card(cards.cards, (remaining[suit][0], suit)),
                                f1_card(cards.cards, (remaining[suit][1], suit)),
                            ][:level],
                            axis=0,
                        ),
                        f2(suits, suit),
                    ],
                    axis=0,
                )
                for suit in fd
            ],
            axis=0,
        )

    return fld


def flush(cards: Cards, board: Board):
    suits = cards.suits
    flush = board.flush

    if len(flush) == 0:
        return cards.empty

    return f2(suits, flush[0])


def flush_h(level):
    def fl(cards: Cards, board: Board):
        suits = cards.suits
        flush = board.flush

        if len(flush) == 0:
            return cards.empty
        remaining = [
            c
            for c in card_values_inv
            if c not in board.cards[board.cards[:, 1] == flush[0]][:, 0]
        ]

        return np.all(
            [
                np.any(
                    [
                        f1_card(cards.cards, (remaining[0], flush[0])),
                        f1_card(cards.cards, (remaining[1], flush[0])),
                        f1_card(cards.cards, (remaining[2], flush[0])),
                        f1_card(cards.cards, (remaining[3], flush[0])),
                    ][:level],
                    axis=0,
                ),
                f2(suits, flush[0]),
            ],
            axis=0,
        )

    return fl


def fb(cards: Cards, board: Board):
    suits = cards.suits

    fb = []
    if len(board.flush) > 0:
        fb = board.flush

    if len(board.fd) > 0:
        fb = board.fd

    if len(fb) == 0:
        return cards.empty

    return np.any(
        [np.all([f1(suits, suit), ~f2(suits, suit)], axis=0) for suit in fb],
        axis=0,
    )


def fb_h(level):
    def flb(cards: Cards, board: Board):
        suits = cards.suits

        fb = []
        if len(board.flush) > 0:
            fb = board.flush

        if len(board.fd) > 0:
            fb = board.fd

        if len(fb) == 0:
            return cards.empty

        remaining = {
            suit: [
                c
                for c in card_values_inv
                if c not in board.cards[board.cards[:, 1] == suit][:, 0]
            ]
            for suit in fb
        }
        return np.any(
            [
                np.any(
                    [
                        np.all(
                            [
                                f1_card(cards.cards, (remaining[suit][0], suit)),
                                ~f2(suits, suit),
                            ],
                            axis=0,
                        ),
                        np.all(
                            [
                                f1_card(cards.cards, (remaining[suit][1], suit)),
                                ~f2(suits, suit),
                            ],
                            axis=0,
                        ),
                        np.all(
                            [
                                f1_card(cards.cards, (remaining[suit][2], suit)),
                                ~f2(suits, suit),
                            ],
                            axis=0,
                        ),
                        np.all(
                            [
                                f1_card(cards.cards, (remaining[suit][3], suit)),
                                ~f2(suits, suit),
                            ],
                            axis=0,
                        ),
                    ][:level],
                    axis=0,
                )
                for suit in fb
            ],
            axis=0,
        )

    return flb


fn = {
    "FD": fd,
    "DFD": dfd,
    "FL": flush,
    "BDFD": bdfd,
    "BDFD2": bdfd_2,
    "FBL": fb,
}
# fn = {f.__name__: f for f in fn}
fn["NF"] = flush_h(1)
fn["NF2"] = flush_h(2)
fn["HF"] = flush_h(4)

fn["NFD"] = fd_h(1)
fn["NFD2"] = fd_h(2)
# fn["fd_h"] = fd_h(4)

fn["NFBL"] = fb_h(1)
fn["NFBL2"] = fb_h(2)
fn["HFBL"] = fb_h(4)
