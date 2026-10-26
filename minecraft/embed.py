import discord

from minecraft.players import fullness_bar, fullness_color, online_names


def motd_text(status):
    motd = status.motd
    return motd.to_plain() if hasattr(motd, "to_plain") else str(motd)


def status_embed(address, status):
    players = status.players
    version = status.version

    embed = discord.Embed(title=address, color=fullness_color(players))
    if motd := motd_text(status):
        embed.description = f"```\n{motd}\n```"

    embed.add_field(name="Players", value=f"`{players.online}/{players.max}`\n`{fullness_bar(players)}`")
    embed.add_field(name="Version", value=f"{version.name}\n*(Protocol: {version.protocol})*")
    embed.add_field(name="Ping", value=f"{status.latency:.0f}ms")

    if names := online_names(players):
        embed.add_field(name="online Players", value=names, inline=False)

    return embed
