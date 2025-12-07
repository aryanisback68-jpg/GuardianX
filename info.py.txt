import discord
from discord.ext import commands
import datetime

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()

    # --- User Info Command ---
    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member}", color=discord.Color.blue())
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="Top Role", value=member.top_role, inline=True)
        embed.add_field(name="Joined Discord", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.set_footer(text="Powered by JC Cheats")
        await ctx.send(embed=embed)

    # --- Server Info Command ---
    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=guild.name, color=discord.Color.green())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Region", value=getattr(guild, 'region', 'Unknown'), inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.set_footer(text="Powered by JC Cheats")
        await ctx.send(embed=embed)

    # --- Avatar Command ---
    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member}'s Avatar", color=discord.Color.purple())
        embed.set_image(url=member.avatar.url)
        embed.set_footer(text="Powered by JC Cheats")
        await ctx.send(embed=embed)

    # --- Banner Command ---
    @commands.command()
    async def banner(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        if member.banner:
            embed = discord.Embed(title=f"{member}'s Banner", color=discord.Color.purple())
            embed.set_image(url=member.banner.url)
            embed.set_footer(text="Powered by JC Cheats")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ {member} does not have a banner! | Powered by JC Cheats")

    # --- Member Count Command ---
    @commands.command()
    async def membercount(self, ctx):
        count = ctx.guild.member_count
        await ctx.send(f"👥 This server has {count} members! | Powered by JC Cheats")

    # --- Uptime Command ---
    @commands.command()
    async def uptime(self, ctx):
        now = datetime.datetime.utcnow()
        delta = now - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"⏱ Bot uptime: {hours}h {minutes}m {seconds}s | Powered by JC Cheats")

def setup(bot):
    bot.add_cog(Info(bot))
