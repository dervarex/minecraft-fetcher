from html import escape

SANS = "Noto Sans, DejaVu Sans, sans-serif"
MONO = "Noto Sans Mono, DejaVu Sans Mono, monospace"


def shorten(text, limit):
    return text if len(text) <= limit else text[: limit - 1] + "…"


def text(x, y, content, size, color="#FFFFFF", bold=False, anchor="start", font=SANS):
    weight = "bold" if bold else "normal"
    return (
        f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" '
        f'font-weight="{weight}" text-anchor="{anchor}">{escape(content)}</text>'
    )


def rect(x, y, width, height, color, radius=0):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{color}"/>'


def image(x, y, size, href):
    return f'<image x="{x}" y="{y}" width="{size}" height="{size}" href="{href}" image-rendering="optimizeSpeed"/>'


def document(width, height, parts):
    body = "\n".join(parts)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n{body}\n</svg>'
