import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") or ""
if not DISCORD_TOKEN:
    raise SystemExit("missing DISCORD_TOKEN in .env")
