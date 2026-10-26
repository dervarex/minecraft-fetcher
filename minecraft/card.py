from html import escape

from minecraft.motd import motd_lines
from minecraft.players import fullness, fullness_color, online_names
from minecraft.svg import MONO, document, image, rect, shorten, text

# that card that gets shown there when /mc <server ip>
WIDTH = 720
HEIGHT = 210
PADDING = 24
ICON_SIZE = 96
CONTENT_X = PADDING + ICON_SIZE + 24
CONTENT_WIDTH = WIDTH - CONTENT_X - PADDING

BACKGROUND = "#1E1F22"
MUTED = "#949BA4"
TRACK = "#2B2D31"


def icon(status):
    if status.icon:
        return image(PADDING, PADDING, ICON_SIZE, status.icon)
    return rect(PADDING, PADDING, ICON_SIZE, ICON_SIZE, TRACK, radius=8)


def header(address, status):
    return [
        text(CONTENT_X, 50, shorten(address, 40), 26, bold=True),
        text(WIDTH - PADDING, 50, f"{status.latency:.0f} ms", 18, MUTED, anchor="end"),
    ]


def motd(status):
    rows = []
    for index, line in enumerate(motd_lines(status.motd)):
        spans = "".join(
            f'<tspan fill="{span.color}" font-weight="{"bold" if span.bold else "normal"}" '
            f'font-style="{"italic" if span.italic else "normal"}">{escape(span.text)}</tspan>'
            for span in line
        )
        y = 84 + index * 22
        rows.append(f'<text x="{CONTENT_X}" y="{y}" font-family="{MONO}" font-size="16" xml:space="preserve">{spans}</text>')
    return rows


def player_bar(status):
    players = status.players
    filled = round(CONTENT_WIDTH * fullness(players))
    return [
        text(CONTENT_X, 150, f"{players.online:,} / {players.max:,} players", 16),
        text(WIDTH - PADDING, 150, shorten(status.version.name, 30), 16, MUTED, anchor="end"),
        rect(CONTENT_X, 160, CONTENT_WIDTH, 10, TRACK, radius=5),
        rect(CONTENT_X, 160, filled, 10, fullness_color(players), radius=5),
    ]


def player_names(status):
    names = online_names(status.players)
    return [text(CONTENT_X, 194, shorten(names, 80), 14, MUTED)] if names else []


def status_card(address, status):
    return document(WIDTH, HEIGHT, [
        rect(0, 0, WIDTH, HEIGHT, BACKGROUND, radius=16),
        icon(status),
        *header(address, status),
        *motd(status),
        *player_bar(status),
        *player_names(status),
    ])
