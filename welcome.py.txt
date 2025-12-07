import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- Welcome New Member ---
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        # Find a channel named 'welcome' or use system channel
        channel = discord.utils.get(guild.text_channels, name="welcome") or guild.system_channel
        if channel:
            embed = discord.Embed(
                title=f"Welcome {member.name}!",
                description=f"👋 Welcome to **{guild.name}**! Enjoy your stay! | Powered by JC Cheats",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url)
            await channel.send(embed=embed)

    # --- Farewell Member ---
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        channel = discord.utils.get(guild.text_channels, name="welcome") or guild.system_channel
        if channel:
            embed = discord.Embed(
                title=f"Goodbye {member.name}",
                description=f"👋 {member.name} has left **{guild.name}**. | Powered by JC Cheats",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url)
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Welcome(bot))
