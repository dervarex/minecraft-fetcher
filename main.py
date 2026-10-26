import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
if not token:
    raise SystemExit("dc token missing in .env")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree


@bot.event
async def on_ready():
    try:
        synced = await tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print("sync failed:", e)
    print(f"logged in as {bot.user}")


@tree.command(name="ping", description="pong")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")



@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    msg = f"error: `{error}`"
    if interaction.response.is_done():
        await interaction.followup.send(msg, ephemeral=True)
    else:
        await interaction.response.send_message(msg, ephemeral=True)


if __name__ == "__main__":
    bot.run(token)
