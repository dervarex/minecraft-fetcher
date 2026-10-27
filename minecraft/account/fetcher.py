import re
from dataclasses import dataclass

import aiohttp

from minecraft.account.mojang import AccountNotFound, download, lookup_skin, lookup_uuid
from minecraft.cache import TimedCache

VALID_NAME = re.compile(r"^[A-Za-z0-9_]{3,16}$") # about the same regex minecraft uses too
TIMEOUT = aiohttp.ClientTimeout(total=5)
recent_accounts = TimedCache(seconds=300)


@dataclass
class Account:
    name: str
    uuid: str
    model: str
    skin: bytes | None


def dashed(uuid):
    return f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"


async def fetch_account(name):
    if not VALID_NAME.match(name):
        raise AccountNotFound

    key = name.lower()
    cached = recent_accounts.get(key)
    if cached:
        return cached

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        name, uuid = await lookup_uuid(session, name)
        skin = await lookup_skin(session, uuid)
        skin_png = await download(session, skin["url"]) if "url" in skin else None

    model = skin.get("metadata", {}).get("model", "classic").upper()
    account = Account(name, dashed(uuid), model, skin_png)
    recent_accounts.set(key, account)
    return account
