import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- Ban Command ---
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"✅ {member.mention} has been banned! | Powered by JC Cheats")

    # --- Kick Command ---
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member.mention} has been kicked! | Powered by JC Cheats")

    # --- Unban Command ---
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"✅ {user.mention} has been unbanned! | Powered by JC Cheats")
                return
        await ctx.send("❌ User not found! | Powered by JC Cheats")

    # --- Mute Command ---
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: int = 0):
        role = get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        await member.add_roles(role)
        msg = f"🔇 {member.mention} has been muted! | Powered by JC Cheats"
        if duration > 0:
            msg += f" for {duration} seconds."
        await ctx.send(msg)
        if duration > 0:
            await asyncio.sleep(duration)
            await member.remove_roles(role)
            await ctx.send(f"✅ {member.mention} has been unmuted after {duration} seconds! | Powered by JC Cheats")

    # --- Softban Command ---
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await member.unban(reason=reason)
        await ctx.send(f"✅ {member.mention} has been softbanned! | Powered by JC Cheats")

    # --- Purge Command ---
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"🧹 Purged {amount} messages! | Powered by JC Cheats", delete_after=5)

    # --- Lock Channel Command ---
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"🔒 {channel.mention} has been locked! | Powered by JC Cheats")

    # --- Unlock Channel Command ---
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"🔓 {channel.mention} has been unlocked! | Powered by JC Cheats")

    # --- Hide Channel Command ---
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def hide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, read_messages=False)
        await ctx.send(f"🙈 {channel.mention} has been hidden! | Powered by JC Cheats")

    # --- Unhide Channel Command ---
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unhide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, read_messages=True)
        await ctx.send(f"👀 {channel.mention} is now visible! | Powered by JC Cheats")

def setup(bot):
    bot.add_cog(Moderation(bot))
