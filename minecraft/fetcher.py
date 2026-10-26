import asyncio

from mcstatus import JavaServer

from minecraft.cache import TimedCache

TIMEOUT_SECONDS = 5.0
recent_statuses = TimedCache(seconds=60)


async def fetch_status(address):
    key = address.lower()
    cached = recent_statuses.get(key)
    if cached:
        return cached

    server = await JavaServer.async_lookup(address)
    status = await asyncio.wait_for(server.async_status(), timeout=TIMEOUT_SECONDS)
    recent_statuses.set(key, status)
    return status
