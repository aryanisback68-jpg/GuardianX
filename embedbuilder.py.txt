import discord
from discord.ext import commands

class EmbedBuilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- Command to create custom embed ---
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def createembed(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        await ctx.send("📝 Enter the **title** of the embed:")
        title_msg = await self.bot.wait_for('message', check=check, timeout=120)
        title = title_msg.content

        await ctx.send("✏️ Enter the **description** of the embed:")
        desc_msg = await self.bot.wait_for('message', check=check, timeout=300)
        description = desc_msg.content

        await ctx.send("🎨 Enter the **hex color** of the embed (e.g., #FF5733):")
        color_msg = await self.bot.wait_for('message', check=check, timeout=120)
        color_hex = color_msg.content.strip()
        try:
            color = int(color_hex.replace("#",""), 16)
        except:
            color = 0x00ff00  # Default green

        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text="Powered by JC Cheats")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

        await ctx.send("✅ Here is your embed preview:", embed=embed)
        await ctx.send("📩 Sending embed to the channel...")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(EmbedBuilder(bot))
