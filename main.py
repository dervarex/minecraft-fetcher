import os
import time
import asyncio
import base64

import discord
from discord import app_commands
from discord.ext import commands

from io import BytesIO
from dotenv import load_dotenv
from mcstatus import JavaServer

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
if not token:
    raise SystemExit("missing DISCORD_TOKEN in .env")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

cache = {}

@bot.event
async def on_ready():
    synced = await tree.sync()

    print(f"synced {len(synced)} global commands")
    print(f"logged in as {bot.user}")

@tree.command(name="ping", description="replies with pong")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

@tree.command(name="mc", description="Get Minecraft server status")
@app_commands.describe(address="Server IP")
@app_commands.checks.cooldown(1, 3.0, key=lambda i: i.user.id)
async def mc(interaction: discord.Interaction, address: str):
    await interaction.response.defer()
    address = address.strip()
    cache_key = address.lower()

    if cache_key in cache and time.time() < cache[cache_key][0]:
        status = cache[cache_key][1]
    else:
        try:
            server = await JavaServer.async_lookup(address)
            status = await asyncio.wait_for(server.async_status(), timeout=5.0)
            cache[cache_key] = (time.time() + 60, status)
        except asyncio.TimeoutError:
            await interaction.followup.send(f"failed to reach `{address}` (timeout)")
            return
        except Exception as e:
            await interaction.followup.send(f"failed to reach `{address}`\nerror: `{type(e).__name__}`")
            return

    online   = status.players.online
    maxp     = status.players.max
    version  = status.version.name
    protocol = status.version.protocol
    latency  = f"{status.latency:.0f}ms"
    motd     = status.motd.to_plain() if hasattr(status.motd, 'to_plain') else str(status.motd)

    percent = (online / maxp) if maxp > 0 else 0
    if percent >= 0.9:
        color = 0xED4245
    elif percent >= 0.5:
        color = 0xFEE75C
    else:
        color = 0x57F287

    filled = int(percent * 10)
    bar = "█" * filled + "░" * (10 - filled)

    embed = discord.Embed(title=f"{address}", color=color)
    if motd:
        embed.description = f"```\n{motd}\n```"

    embed.add_field(name="Players", value=f"`{online}/{maxp}`\n`{bar}`", inline=True)
    embed.add_field(name="Version", value=f"{version}\n*(Protocol: {protocol})*", inline=True)
    embed.add_field(name="Ping", value=latency, inline=True)

    if getattr(status.players, "sample", None):
        names = [p.name for p in status.players.sample]
        if len(names) > 5:
            player_list = ", ".join(names[:5]) + f" and {len(names)-5} more"
        else:
            player_list = ", ".join(names)
        embed.add_field(name="online Players", value=player_list, inline=False)

    if getattr(status, "icon", None):
        icon_data = status.icon.split(",")[1] if "," in status.icon else status.icon
        file = discord.File(BytesIO(base64.b64decode(icon_data)), filename="icon.png")
        embed.set_thumbnail(url="attachment://icon.png")
        await interaction.followup.send(embed=embed, file=file)
    else:
        await interaction.followup.send(embed=embed)

@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    msg = f"wait {error.retry_after:.1f}s." if isinstance(error, app_commands.CommandOnCooldown) else f"error: `{error}`"
    if interaction.response.is_done():
        await interaction.followup.send(msg, ephemeral=True)
    else:
        await interaction.response.send_message(msg, ephemeral=True)

if __name__ == "__main__":
    bot.run(token)
