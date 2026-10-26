from mcstatus.motd import Motd

RED = "#ED4245"
YELLOW = "#FEE75C"
GREEN = "#57F287"

MAX_LISTED_NAMES = 5


def fullness(players):
    return min(players.online / players.max, 1) if players.max > 0 else 0


def fullness_color(players):
    percent = fullness(players)
    if percent >= 0.9:
        return RED
    if percent >= 0.5:
        return YELLOW
    return GREEN


def online_names(players):
    names = [Motd.parse(p.name).to_plain() for p in getattr(players, "sample", None) or []]
    if len(names) > MAX_LISTED_NAMES:
        hidden = len(names) - MAX_LISTED_NAMES
        return ", ".join(names[:MAX_LISTED_NAMES]) + f" and {hidden} more"
    return ", ".join(names)
