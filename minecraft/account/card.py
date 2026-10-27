from drawing.svg import MONO, document, rect, text
from minecraft.account.skin import skin_figure

# card rendering

WIDTH = 600
HEIGHT = 340
PADDING = 24
SKIN_SCALE = 8
SKIN_WIDTH = 16 * SKIN_SCALE
SKIN_HEIGHT = 32 * SKIN_SCALE
CONTENT_X = PADDING + SKIN_WIDTH + 40

BACKGROUND = "#1E1F22"
MUTED = "#949BA4"


def skin_column(account):
    label_y = PADDING + SKIN_HEIGHT + 26
    return [
        skin_figure(account.skin, account.model == "SLIM", PADDING, PADDING, SKIN_SCALE),
        text(PADDING + SKIN_WIDTH / 2, label_y, account.model, 11, MUTED, anchor="middle"),
    ]


def details(account):
    return [
        text(CONTENT_X, 80, account.name, 34, bold=True),
        text(CONTENT_X, 132, "UUID", 13, MUTED, bold=True),
        text(CONTENT_X, 156, account.uuid, 15, font=MONO),
    ]


def account_card(account):
    return document(WIDTH, HEIGHT, [
        rect(0, 0, WIDTH, HEIGHT, BACKGROUND, radius=16),
        *skin_column(account),
        *details(account),
    ])
