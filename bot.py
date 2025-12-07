import discord
from discord.ext import commands, tasks
import os, random

TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    raise Exception("BOT_TOKEN not set in Render Environment!")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

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
    print(f"{bot.user} is online!")
    change_status.start()

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🟢")

bot.run(TOKEN)
