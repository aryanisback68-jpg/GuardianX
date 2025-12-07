import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Helper: Get mod-log channel
    def get_log_channel(self, guild):
        return discord.utils.get(guild.text_channels, name="mod-logs") or guild.system_channel

    # --- Message Delete ---
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        channel = self.get_log_channel(message.guild)
        if channel:
            embed = discord.Embed(
                title="Message Deleted",
                description=f"User: {message.author.mention}\nChannel: {message.channel.mention}\nContent: {message.content}",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by JC Cheats")
            await channel.send(embed=embed)

    # --- Message Edit ---
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        if before.content == after.content:
            return
        channel = self.get_log_channel(before.guild)
        if channel:
            embed = discord.Embed(
                title="Message Edited",
                description=f"User: {before.author.mention}\nChannel: {before.channel.mention}\nBefore: {before.content}\nAfter: {after.content}",
                color=discord.Color.orange()
            )
            embed.set_footer(text="Powered by JC Cheats")
            await channel.send(embed=embed)

    # --- Member Join ---
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.get_log_channel(member.guild)
        if channel:
            embed = discord.Embed(
                title="Member Joined",
                description=f"User: {member.mention} ({member.name}) has joined the server.",
                color=discord.Color.green()
            )
            embed.set_footer(text="Powered by JC Cheats")
            await channel.send(embed=embed)

    # --- Member Leave ---
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.get_log_channel(member.guild)
        if channel:
            embed = discord.Embed(
                title="Member Left",
                description=f"User: {member.mention} ({member.name}) has left the server.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by JC Cheats")
            await channel.send(embed=embed)

    # --- Role Changes ---
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        channel = self.get_log_channel(role.guild)
        if channel:
            embed = discord.Embed(
                title="Role Created",
                description=f"Role: {role.name} has been created.",
                color=discord.Color.green()
            )
            embed.set_footer(text="Powered by JC Cheats")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        channel = self.get_log_channel(role.guild)
        if channel:
            embed = discord.Embed(
                title="Role Deleted",
                description=f"Role: {role.name} has been deleted.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by JC Cheats")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        channel = self.get_log_channel(before.guild)
        if channel:
            embed = discord.Embed(
                title="Role Updated",
                description=f"Role: {before.name}\nBefore: {before.permissions}\nAfter: {after.permissions}",
                color=discord.Color.orange()
            )
            embed.set_footer(text="Powered by JC Cheats")
            await channel.send(embed=embed)

    # --- Member Ban ---
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = self.get_log_channel(guild)
        if channel:
            embed = discord.Embed(
                title="Member Banned",
                description=f"User: {user.mention} has been banned.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by JC Cheats")
            await channel.send(embed=embed)

    # --- Member Unban ---
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = self.get_log_channel(guild)
        if channel:
            embed = discord.Embed(
                title="Member Unbanned",
                description=f"User: {user.mention} has been unbanned.",
                color=discord.Color.green()
            )
            embed.set_footer(text="Powered by JC Cheats")
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Logs(bot))
