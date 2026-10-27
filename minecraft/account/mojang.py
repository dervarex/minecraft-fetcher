import base64
import json

import aiohttp

UUID_URL = "https://api.mojang.com/users/profiles/minecraft/{name}" # returns "id" and "name". id is the uuid without dashes
PROFILE_URL = "https://sessionserver.mojang.com/session/minecraft/profile/{uuid}" # returns the same as above,
# and more base64 encoded data: timestamp, profileId (same as id field), profileName (same as name field) and the skin texture url


class AccountNotFound(Exception):
    pass


async def get_json(session: aiohttp.ClientSession, url):
    async with session.get(url) as response:
        if response.status in (204, 404):
            raise AccountNotFound
        response.raise_for_status()
        return await response.json()


async def lookup_uuid(session, name):
    profile = await get_json(session, UUID_URL.format(name=name))
    return profile["name"], profile["id"]


async def lookup_skin(session, uuid):
    profile = await get_json(session, PROFILE_URL.format(uuid=uuid))
    encoded = profile["properties"][0]["value"]
    textures = json.loads(base64.b64decode(encoded))["textures"]
    return textures.get("SKIN", {})


async def download(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.read()
