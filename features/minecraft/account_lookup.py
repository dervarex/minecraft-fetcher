import asyncio
from io import BytesIO

import discord
from discord import app_commands
from discord.ext import commands

from drawing.png import svg_to_png
from minecraft.account.card import account_card
from minecraft.account.fetcher import fetch_account
from minecraft.account.mojang import AccountNotFound

# since discord can't do that 3d view thing, lets just link namemc, maybe later own gh pages thing but it works for now
NAMEMC_URL = "https://namemc.com/profile/{uuid}"


def view_3d_button(account):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="View 3D", url=NAMEMC_URL.format(uuid=account.uuid)))
    return view


# Account Lookup, takes data from official mojang api and links namemc for 3d view
class AccountLookup(commands.Cog):
    @app_commands.command(name="account", description="get a minecraft account's uuid and skin")
    @app_commands.describe(name="minecraft username")
    @app_commands.checks.cooldown(1, 3.0, key=lambda i: i.user.id)
    async def account(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer()
        name = name.strip()

        try:
            account = await fetch_account(name)
        except AccountNotFound:
            await interaction.followup.send(f"no account named `{name}`")
            return
        except Exception as e:
            await interaction.followup.send(f"failed to look up `{name}`\nerror: `{type(e).__name__}`")
            return

        png = await asyncio.to_thread(svg_to_png, account_card(account))
        file = discord.File(BytesIO(png), filename="account.png")
        await interaction.followup.send(file=file, view=view_3d_button(account))


async def setup(bot):
    await bot.add_cog(AccountLookup())
