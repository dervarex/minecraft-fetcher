import discord
from discord.ext import commands

from bot.loader import all_feature_modules


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self):
        for module in all_feature_modules():
            await self.load_extension(module)
        synced = await self.tree.sync()
        print(f"synced {len(synced)} global commands")

    async def on_ready(self):
        print(f"logged in as {self.user}")
