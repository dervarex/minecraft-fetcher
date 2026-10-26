import discord
from discord import app_commands


def error_message(error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        return f"wait {error.retry_after:.1f}s."
    return f"error: `{error}`"


async def reply_with_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    message = error_message(error)
    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


async def setup(bot):
    bot.tree.on_error = reply_with_error
