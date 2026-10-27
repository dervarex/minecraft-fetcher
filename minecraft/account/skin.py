import base64
import struct

# Skin rendering. props to claude for this one, i hate rendering

PLACEHOLDER = "#3F4147"


def skin_height(png):
    width, height = struct.unpack(">II", png[16:24])
    return height * 64 // width


def crop(x, y, width, height, source_x, source_y, mirrored=False):
    part = (
        f'<svg x="{x}" y="{y}" width="{width}" height="{height}" '
        f'viewBox="{source_x} {source_y} {width} {height}" preserveAspectRatio="none">'
        f'<use href="#skin"/></svg>'
    )
    if mirrored:
        return f'<g transform="translate({2 * x + width} 0) scale(-1 1)">{part}</g>'
    return part


def front_parts(arm, legacy):
    base = [
        crop(4, 0, 8, 8, 8, 8),
        crop(4, 8, 8, 12, 20, 20),
        crop(4 - arm, 8, arm, 12, 44, 20),
        crop(4, 20, 4, 12, 4, 20),
    ]
    if legacy:
        return base + [
            crop(12, 8, arm, 12, 44, 20, mirrored=True),
            crop(8, 20, 4, 12, 4, 20, mirrored=True),
            crop(4, 0, 8, 8, 40, 8),
        ]
    return base + [
        crop(12, 8, arm, 12, 36, 52),
        crop(8, 20, 4, 12, 20, 52),
        crop(4, 0, 8, 8, 40, 8),
        crop(4, 8, 8, 12, 20, 36),
        crop(4 - arm, 8, arm, 12, 44, 36),
        crop(12, 8, arm, 12, 52, 52),
        crop(4, 20, 4, 12, 4, 36),
        crop(8, 20, 4, 12, 4, 52),
    ]


def silhouette(arm):
    boxes = [(4, 0, 8, 8), (4, 8, 8, 12), (4 - arm, 8, arm, 12), (12, 8, arm, 12), (4, 20, 8, 12)]
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PLACEHOLDER}"/>' for x, y, w, h in boxes]


def skin_figure(png, slim, x, y, scale):
    arm = 3 if slim else 4
    if png is None:
        parts = silhouette(arm)
    else:
        height = skin_height(png)
        href = "data:image/png;base64," + base64.b64encode(png).decode()
        parts = [
            f'<defs><image id="skin" width="64" height="{height}" href="{href}" image-rendering="optimizeSpeed"/></defs>',
            *front_parts(arm, legacy=height == 32),
        ]
    body = "".join(parts)
    return f'<g transform="translate({x} {y}) scale({scale})">{body}</g>'
