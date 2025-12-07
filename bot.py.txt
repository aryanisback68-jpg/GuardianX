import discord
from discord.ext import commands, tasks
import json, os, random

# Load config
with open("config.json") as f:
    config = json.load(f)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["prefix"], intents=intents, help_command=None)

# Load all cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# Status rotation
@tasks.loop(minutes=10)
async def change_status():
    statuses = [
        "GuardianX Protecting Servers | Powered by JC Cheats",
        "Use !help for commands",
        "Powered by JC Cheats"
    ]
    await bot.change_presence(activity=discord.Game(name=random.choice(statuses)))

@bot.event
async def on_ready():
    print(f"{bot.user} is online! | Powered by JC Cheats")
    change_status.start()

bot.run(config["token"])
