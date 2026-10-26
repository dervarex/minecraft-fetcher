import resvg_py

ZOOM = 2

# svg to png converter
def svg_to_png(svg):
    return bytes(resvg_py.svg_to_bytes(svg_string=svg, zoom=ZOOM))
