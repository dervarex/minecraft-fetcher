import base64
from io import BytesIO

import discord


def icon_file(status):
    icon = getattr(status, "icon", None)
    if not icon:
        return None
    image_data = icon.split(",")[-1]
    return discord.File(BytesIO(base64.b64decode(image_data)), filename="icon.png")
