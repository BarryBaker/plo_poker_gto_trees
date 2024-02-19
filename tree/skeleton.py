from omaha._cards import Board


def skeleton(
    b: Board, hand_before: list[tuple], result: list[tuple], is_attack: bool, columns, pot
):
    hand_before = [(i[0][0], i[1]) for i in hand_before]
    street = "flop"
    if len(b.cards) == 4:
        street = "turn"

    def build_skeleton(sk: list, filters):
        elements_1 = [next(iter(i)) if isinstance(i, dict) else i for i in sk]
        elements = [i for i in elements_1 if i in list(columns)]
        # elements = [i for i in elements if len([j for j in result if j[0] == i]) > 0]
        for index, label in enumerate(elements):
            h = filters + [(i, 0) for i in elements[:index]]
            to_return = None
            if isinstance(sk[elements_1.index(label)], dict):
                # try:
                to_return = build_skeleton(
                    sk[elements_1.index(label)][label], h + [(label, 1)]
                )
                # except:
                #     print(sk, elements, index, label)
            if to_return:
                return to_return
            if hand_before == h:
                to_return = [i for i in result if i[0] == label]

                return to_return

    if (
        not b.is_paired
        and not b.is_flush
        and not b.is_str8
        and not b.is_suited
        and is_attack
        and street == "flop"
        and pot == "SRP"
    ):
        return build_skeleton(
            [
                "TRIPS",
                "2PT",
                {
                    "SDBL": [
                        {"SD": ["WR", "OESD"]},
                    ]
                },
                "BOP",
            ],
            [],
        )

    if (
        not b.is_paired
        and not b.is_flush
        and not b.is_str8
        and not b.is_suited
        and is_attack
    ):
        return build_skeleton(
            [
                "TRIPS",
                "2P",
                {"SD": ["WR", "OESD"]},
                {"SDBL": ["DSDBL"]},
                "BOP",
            ],
            [],
        )
    if (
        not b.is_paired
        and not b.is_flush
        and not b.is_str8
        and not b.is_suited
        and not is_attack
    ):
        return build_skeleton(
            [
                "TRIPS",
                "2P",
                {"SD": ["WR", "OESD"]},
                "BOP",
            ],
            [],
        )
    if (
        not b.is_paired
        and not b.is_flush
        and not b.is_str8
        # and b.is_suited
        and is_attack
        and street == "flop"
        and pot == "3BP"
    ):
        return build_skeleton(
            [
                "TRIPS",
                "2P",
                "FD",
                "FBL",
                {"SD": ["WR", "OESD"]},
                "BOP",
            ],
            [],
        )
    if (
        not b.is_paired
        and not b.is_flush
        and not b.is_str8
        and b.is_suited
        and is_attack
        and street == "flop"
    ):
        return build_skeleton(
            [
                "TRIPS",
                "2PT",
                "WR",
                "FD",
                "FBL",
                "BOP",
            ],
            [],
        )
    if (
        not b.is_paired
        and not b.is_flush
        and not b.is_str8
        and b.is_suited
        and is_attack
        and street == "turn"
    ):
        return build_skeleton(
            [
                "TRIPS",
                "2P",
                "FD",
                "FBL",
                "SD",
                "BOP",
            ],
            [],
        )
    if (
        not b.is_paired
        and not b.is_flush
        and not b.is_str8
        and b.is_suited
        and not is_attack
    ):
        return build_skeleton(
            [
                "TRIPS",
                "2P",
                "FD",
                {"SD": ["WR", "OESD"]},
            ],
            [],
        )

    """Paired"""

    if (
        b.is_paired
        and not b.is_flush
        and not b.is_str8
        and not b.is_suited
        and is_attack
        and street == "flop"
    ):
        return build_skeleton(
            ["FULL", "TRIPS", "RR", {"SD": ["WR", "OESD"]}, "OP", "TP", "BDFD"],
            [],
        )
    if (
        b.is_paired
        and not b.is_flush
        and not b.is_str8
        and not b.is_suited
        and is_attack
        and street == "turn"
    ):
        return build_skeleton(
            ["FULL", "TRIPS", "OP", "BOP", "RR", {"SD": ["WR", "OESD"]}],
            [],
        )
    if (
        b.is_paired
        and not b.is_flush
        and not b.is_str8
        and not b.is_suited
        and not is_attack
    ):
        return build_skeleton(
            ["FULL", "TRIPS", "OP", {"SD": ["WR", "OESD"]}, "RR", "TP"],
            [],
        )
    if (
        b.is_paired
        and not b.is_flush
        and not b.is_str8
        and b.is_suited
        and is_attack
        and street == "flop"
    ):
        return build_skeleton(
            [
                "FULL",
                "TRIPS",
                "RR",
                {"FD": ["NFD"]},
                {"SD": ["WR", "OESD"]},
                "OP",
                "TP",
                "BDFD",
            ],
            [],
        )
    if (
        b.is_paired
        and not b.is_flush
        and not b.is_str8
        and b.is_suited
        and is_attack
        and street == "turn"
    ):
        return build_skeleton(
            [
                "FULL",
                "TRIPS",
                {"FD": ["NFD"]},
                {"SD": ["WR", "OESD"]},
                "OP",
                "BOP",
            ],
            [],
        )
    if b.is_paired and not b.is_flush and not b.is_str8 and b.is_suited and not is_attack:
        return build_skeleton(
            ["FULL", "TRIPS", "OP", "FD", {"SD": ["WR", "OESD"]}, "RR", "TP"],
            [],
        )

    """ Turn paireds"""

    if b.is_paired and not b.is_flush and b.is_str8 and not b.is_suited:
        return build_skeleton(
            ["FULL", "STR", "TRIPS", {"SD": ["WR", "OESD"]}, "OP", "BOP", "RR"],
            [],
        )
    if b.is_paired and not b.is_flush and b.is_str8 and b.is_suited:
        return build_skeleton(
            ["FULL", "STR", "TRIPS", "FD", {"SD": ["WR", "OESD"]}, "OP", "BOP", "RR"],
            [],
        )
    if b.is_paired and not b.is_flush and b.is_str8 and not b.is_suited:
        return build_skeleton(
            ["FULL", "STR", "TRIPS", {"SD": ["WR", "OESD"]}, "OP", "BOP", "RR"],
            [],
        )
    if b.is_paired and b.is_flush:
        return build_skeleton(
            ["FULL", "FL", "STR", "TRIPS", "FBL", "OP", "BOP", "RR"],
            [],
        )
    """Str8"""

    if not b.is_paired and not b.is_flush and b.is_str8 and not b.is_suited and is_attack:
        return build_skeleton(
            [
                "STR",
                {"SDBL": ["TRIPS", "2P", "SD", "BOP"]},
                "TRIPS",
                "2P",
                "BOP",
            ],
            [],
        )
    if (
        not b.is_paired
        and not b.is_flush
        and b.is_str8
        and not b.is_suited
        and not is_attack
    ):
        return build_skeleton(
            [
                "STR",
                "TRIPS",
                "2P",
                "SD",
                "BOP",
            ],
            [],
        )
    if not b.is_paired and not b.is_flush and b.is_str8 and b.is_suited and is_attack:
        return build_skeleton(
            [
                "STR",
                {"SDBL": ["TRIPS", "2P", "FD", "FBL", "SD", "BOP"]},
                "TRIPS",
                "2P",
                "FD",
                "FBL",
                "BOP",
            ],
            [],
        )
    if not b.is_paired and not b.is_flush and b.is_str8 and b.is_suited and not is_attack:
        return build_skeleton(
            [
                "STR",
                "TRIPS",
                "2P",
                "FD",
                "SD",
                "BOP",
            ],
            [],
        )
    if b.is_paired and b.is_flush and not b.is_str8:
        return build_skeleton(
            [
                "FULL",
                "FL",
                "TRIPS",
                "FBL",
                "BOP",
            ],
            [],
        )
    if b.is_paired and b.is_flush and b.is_str8:
        return build_skeleton(
            [
                "FULL",
                "FL",
                "STR",
                "TRIPS",
                "FBL",
                "BOP",
            ],
            [],
        )
    if b.is_flush:
        return build_skeleton(
            ["FL", "FBL", "STR", "TRIPS", "2P", "SD"],
            [],
        )
