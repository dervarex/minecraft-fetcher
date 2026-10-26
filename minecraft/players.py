RED = 0xED4245
YELLOW = 0xFEE75C
GREEN = 0x57F287

MAX_LISTED_NAMES = 5
BAR_LENGTH = 10


def fullness(players):
    return players.online / players.max if players.max > 0 else 0


def fullness_color(players):
    percent = fullness(players)
    if percent >= 0.9:
        return RED
    if percent >= 0.5:
        return YELLOW
    return GREEN


def fullness_bar(players):
    filled = int(fullness(players) * BAR_LENGTH)
    return "█" * filled + "░" * (BAR_LENGTH - filled)


def online_names(players):
    names = [p.name for p in getattr(players, "sample", None) or []]
    if len(names) > MAX_LISTED_NAMES:
        hidden = len(names) - MAX_LISTED_NAMES
        return ", ".join(names[:MAX_LISTED_NAMES]) + f" and {hidden} more"
    return ", ".join(names)
