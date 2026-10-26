import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from minecraft.fetcher import fetch_status
from minecraft.embed import status_embed
from minecraft.icon import icon_file


class ServerStatus(commands.Cog):
    @app_commands.command(name="mc", description="get minecraft server status")
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

        embed = status_embed(address, status)
        icon = icon_file(status)
        if icon:
            embed.set_thumbnail(url=f"attachment://{icon.filename}")
            await interaction.followup.send(embed=embed, file=icon)
        else:
            await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerStatus())
