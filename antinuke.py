import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio

# Anti-Nuke configuration
MAX_BANS = 3          # Max bans allowed per user in 10 seconds
MAX_KICKS = 3         # Max kicks allowed per user in 10 seconds
MAX_ROLE_DELETES = 2  # Max role deletions per user in 10 seconds
CHECK_INTERVAL = 10   # Time window in seconds

class AntiNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ban_tracker = {}
        self.kick_tracker = {}
        self.role_delete_tracker = {}

    # --- Ban detection and protection ---
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        # Who banned this member?
        async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=1):
            executor = entry.user
            if executor == guild.me or executor == guild.owner:
                return
            self.ban_tracker.setdefault(executor.id, [])
            self.ban_tracker[executor.id].append(entry.created_at)
            # Remove old timestamps
            self.ban_tracker[executor.id] = [t for t in self.ban_tracker[executor.id] if (entry.created_at - t).total_seconds() <= CHECK_INTERVAL]
            if len(self.ban_tracker[executor.id]) > MAX_BANS:
                try:
                    await executor.kick(reason="Mass banning detected")
                    await guild.owner.send(f"⚠️ {executor} was kicked for mass banning in {guild.name}! | Powered by JC Cheats")
                except:
                    await guild.owner.send(f"⚠️ Could not punish {executor} for mass banning in {guild.name}! | Powered by JC Cheats")

    # --- Kick detection and protection ---
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        async for entry in guild.audit_logs(action=discord.AuditLogAction.kick, limit=1):
            executor = entry.user
            if executor == guild.me or executor == guild.owner:
                return
            self.kick_tracker.setdefault(executor.id, [])
            self.kick_tracker[executor.id].append(entry.created_at)
            self.kick_tracker[executor.id] = [t for t in self.kick_tracker[executor.id] if (entry.created_at - t).total_seconds() <= CHECK_INTERVAL]
            if len(self.kick_tracker[executor.id]) > MAX_KICKS:
                try:
                    await executor.kick(reason="Mass kicking detected")
                    await guild.owner.send(f"⚠️ {executor} was kicked for mass kicking in {guild.name}! | Powered by JC Cheats")
                except:
                    await guild.owner.send(f"⚠️ Could not punish {executor} for mass kicking in {guild.name}! | Powered by JC Cheats")

    # --- Role deletion detection ---
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild = role.guild
        async for entry in guild.audit_logs(action=discord.AuditLogAction.role_delete, limit=1):
            executor = entry.user
            if executor == guild.me or executor == guild.owner:
                return
            self.role_delete_tracker.setdefault(executor.id, [])
            self.role_delete_tracker[executor.id].append(entry.created_at)
            self.role_delete_tracker[executor.id] = [t for t in self.role_delete_tracker[executor.id] if (entry.created_at - t).total_seconds() <= CHECK_INTERVAL]
            if len(self.role_delete_tracker[executor.id]) > MAX_ROLE_DELETES:
                try:
                    await executor.kick(reason="Mass role deletion detected")
                    await guild.owner.send(f"⚠️ {executor} was kicked for mass role deletion in {guild.name}! | Powered by JC Cheats")
                except:
                    await guild.owner.send(f"⚠️ Could not punish {executor} for mass role deletion in {guild.name}! | Powered by JC Cheats")
        # Optional: Restore the deleted role
        try:
            new_role = await guild.create_role(name=role.name, permissions=role.permissions, colour=role.colour)
            await guild.owner.send(f"✅ Role '{role.name}' restored! | Powered by JC Cheats")
        except:
            await guild.owner.send(f"❌ Failed to restore role '{role.name}'! | Powered by JC Cheats")

def setup(bot):
    bot.add_cog(AntiNuke(bot))
