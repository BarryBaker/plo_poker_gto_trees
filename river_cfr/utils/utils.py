def river_cat(riverboard):
    if riverboard.flush:
        if riverboard.paired:
            return "flush_paired"
        else:
            return "flush"
    elif riverboard.str8:
        if riverboard.paired:
            return "str8_paired"
        else:
            return "str8"
    elif riverboard.paired:
        return "paired"
    else:
        return "unpaired"
