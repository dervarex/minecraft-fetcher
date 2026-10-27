import asyncio
from io import BytesIO

import discord
from discord import app_commands
from discord.ext import commands

from minecraft.server.card import status_card
from minecraft.server.fetcher import fetch_status
from drawing.png import svg_to_png


# gets a minecraft server's status, like your game client would
class ServerStatus(commands.Cog):
    @app_commands.command(name="server", description="get minecraft server status")
    @app_commands.describe(address="server ip")
    @app_commands.checks.cooldown(1, 3.0, key=lambda i: i.user.id)
    async def mc(self, interaction: discord.Interaction, address: str):
        await interaction.response.defer()
        address = address.strip()

        try:
            status = await fetch_status(address)
        except asyncio.TimeoutError:
            await interaction.followup.send(f"failed to reach `{address}` (timeout)")
            return
        except Exception as e:
            await interaction.followup.send(f"failed to reach `{address}`\nerror: `{type(e).__name__}`")
            return

        png = await asyncio.to_thread(svg_to_png, status_card(address, status))
        await interaction.followup.send(file=discord.File(BytesIO(png), filename="status.png"))


async def setup(bot):
    await bot.add_cog(ServerStatus())
