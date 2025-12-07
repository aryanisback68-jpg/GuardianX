import discord
from discord.ext import commands, tasks
import itertools

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Define rotating statuses
        self.statuses = itertools.cycle([
            "Protecting your server | Powered by JC Cheats",
            "Type !help for commands | JC Cheats",
            "GuardianX at your service | Powered by JC Cheats",
            "Keeping servers safe | JC Cheats"
        ])
        self.change_status.start()

    # --- Task to rotate status every 30 seconds ---
    @tasks.loop(seconds=30)
    async def change_status(self):
        new_status = next(self.statuses)
        await self.bot.change_presence(activity=discord.Game(name=new_status))

    # --- Stop the task when cog is unloaded ---
    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Status(bot))
