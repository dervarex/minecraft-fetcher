from dataclasses import dataclass, replace

from mcstatus.motd import Motd
from mcstatus.motd.components import JavaFormatting, JavaMinecraftColor, WebColor

DEFAULT_COLOR = "#AAAAAA"

COLOR_HEX = {
    JavaMinecraftColor.BLACK: "#000000",
    JavaMinecraftColor.DARK_BLUE: "#0000AA",
    JavaMinecraftColor.DARK_GREEN: "#00AA00",
    JavaMinecraftColor.DARK_AQUA: "#00AAAA",
    JavaMinecraftColor.DARK_RED: "#AA0000",
    JavaMinecraftColor.DARK_PURPLE: "#AA00AA",
    JavaMinecraftColor.GOLD: "#FFAA00",
    JavaMinecraftColor.GRAY: "#AAAAAA",
    JavaMinecraftColor.DARK_GRAY: "#555555",
    JavaMinecraftColor.BLUE: "#5555FF",
    JavaMinecraftColor.GREEN: "#55FF55",
    JavaMinecraftColor.AQUA: "#55FFFF",
    JavaMinecraftColor.RED: "#FF5555",
    JavaMinecraftColor.LIGHT_PURPLE: "#FF55FF",
    JavaMinecraftColor.YELLOW: "#FFFF55",
    JavaMinecraftColor.WHITE: "#FFFFFF",
}


@dataclass
class Span:
    text: str = ""
    color: str = DEFAULT_COLOR
    bold: bool = False
    italic: bool = False


def motd_lines(motd: Motd, max_lines=2):
    lines: list[list[Span]] = [[]]
    style = Span()
    for part in motd.parsed:
        if isinstance(part, str):
            first, *rest = part.split("\n")
            lines[-1].append(replace(style, text=first))
            lines += [[replace(style, text=text)] for text in rest]
        elif isinstance(part, JavaMinecraftColor):
            style = Span(color=COLOR_HEX[part])
        elif isinstance(part, WebColor):
            style = Span(color=part.hex)
        elif part == JavaFormatting.BOLD:
            style = replace(style, bold=True)
        elif part == JavaFormatting.ITALIC:
            style = replace(style, italic=True)
        elif part == JavaFormatting.RESET:
            style = Span()
    return lines[:max_lines]
