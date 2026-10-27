# Minecraft Utility Bot

A Discord bot with (useful) Minecraft tools

## Commands

|      Command      |             What it does              |
| ----------------- | ------------------------------------- |
| `/mc <address>`   | Shows a server's status and some info |
| `/account <name>` | Shows a player's uuid, skin and model |
| `/ping`           | Ask bot if he's alive                 |

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "DISCORD_TOKEN=here-insert-token" > .env
python main.py
```

## Project layout

```
bot/         bot startup stuff
features/    slash commands, one file per cmd
minecraft/   minecraft logic
drawing/     svg + png helpers for the images
```
