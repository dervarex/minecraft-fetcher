import discord
from discord import app_commands
from discord.ext import commands

# Simple Ping thing. will be removed eventually, just for debug
class Ping(commands.Cog):
    @app_commands.command(name="ping", description="replies with pong")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong!")


async def setup(bot):
    await bot.add_cog(Ping())
