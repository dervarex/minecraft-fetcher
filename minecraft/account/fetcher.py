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
    url: str | None


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
        canonical_name, uuid = await lookup_uuid(session, name)
        skin = await lookup_skin(session, uuid)
        url = skin.get("url")
        skin_png = await download(session, url) if url else None

    model = skin.get("metadata", {}).get("model", "classic").upper()
    account = Account(canonical_name, dashed(uuid), model, skin_png, url)
    recent_accounts.set(key, account)
    return account


async def fetch_skin_file(name):
    return (await fetch_account(name)).url
