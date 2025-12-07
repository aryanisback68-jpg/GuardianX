import discord
from discord.ext import tasks
from discord import app_commands
import os
import random

TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    raise Exception("BOT_TOKEN not set in Render!")

intents = discord.Intents.all()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# =====================================================================
# STATUS ROTATION
# =====================================================================
@tasks.loop(seconds=30)
async def rotate_status():
    statuses = [
        "GuardianX Protecting Servers",
        "Use /help",
        "Powered by JC Cheats"
    ]
    await bot.change_presence(
        activity=discord.Game(random.choice(statuses))
    )

# =====================================================================
# READY EVENT
# =====================================================================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await tree.sync()
    print("Slash Commands Synced.")
    rotate_status.start()

# =====================================================================
# HELP COMMAND
# =====================================================================
@tree.command(name="help", description="Show all commands")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="GuardianX - Help Menu",
        description="All available commands",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🔒 Moderation",
        value="/kick • /ban • /clear • /mute • /unmute",
        inline=False
    )

    embed.add_field(
        name="🛡 Antinuke",
        value="/antinuke-status • /antinuke-enable • /antinuke-disable",
        inline=False
    )

    embed.add_field(
        name="🤖 AutoMod",
        value="/automod-status • /automod-enable • /automod-disable",
        inline=False
    )

    embed.add_field(
        name="🎫 Ticket",
        value="/ticket-open • /ticket-close",
        inline=False
    )

    await interaction.response.send_message(embed=embed)

# =====================================================================
# MODERATION COMMANDS
# =====================================================================

@tree.command(name="kick", description="Kick a member")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"Kicked {member.mention} ✔")

@tree.command(name="ban", description="Ban a member")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"Banned {member.mention} ✔")

@tree.command(name="clear", description="Clear messages")
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"Cleared {amount} messages ✔", ephemeral=True)

# =====================================================================
# AUTOMOD COMMANDS
# =====================================================================

automod_enabled = False

@tree.command(name="automod-enable", description="Enable automod")
async def automod_enable(interaction: discord.Interaction):
    global automod_enabled
    automod_enabled = True
    await interaction.response.send_message("AutoMod Enabled ✔")

@tree.command(name="automod-disable", description="Disable automod")
async def automod_disable(interaction: discord.Interaction):
    global automod_enabled
    automod_enabled = False
    await interaction.response.send_message("AutoMod Disabled ✔")

@tree.command(name="automod-status", description="Check automod status")
async def automod_status(interaction: discord.Interaction):
    status = "Enabled" if automod_enabled else "Disabled"
    await interaction.response.send_message(f"AutoMod is **{status}**")

# AUTOMOD FILTER SYSTEM
bad_words = ["fuck", "madarchod", "gaand", "chutiya"]

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if automod_enabled:
        if any(word in message.content.lower() for word in bad_words):
            await message.delete()
            await message.channel.send(f"{message.author.mention} Don't use bad words!", delete_after=3)

# =====================================================================
# ANTINUKE COMMANDS
# =====================================================================

antinuke_enabled = False

@tree.command(name="antinuke-enable", description="Enable antinuke system")
async def antinuke_enable(interaction: discord.Interaction):
    global antinuke_enabled
    antinuke_enabled = True
    await interaction.response.send_message("AntiNuke Enabled ✔")

@tree.command(name="antinuke-disable", description="Disable antinuke system")
async def antinuke_disable(interaction: discord.Interaction):
    global antinuke_enabled
    antinuke_enabled = False
    await interaction.response.send_message("AntiNuke Disabled ✔")

@tree.command(name="antinuke-status", description="Check antinuke status")
async def antinuke_status(interaction: discord.Interaction):
    status = "Enabled" if antinuke_enabled else "Disabled"
    await interaction.response.send_message(f"AntiNuke is **{status}**")

# BASIC ANTINUKE EVENT (role delete protection)
@bot.event
async def on_guild_role_delete(role):
    if antinuke_enabled:
        log = role.guild.system_channel
        if log:
            await log.send(f"⚠ Role `{role.name}` was deleted!")

# =====================================================================
# TICKET SYSTEM
# =====================================================================

@tree.command(name="ticket-open", description="Open a support ticket")
async def ticket_open(interaction: discord.Interaction):
    guild = interaction.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True)
    }
    channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites)
    await interaction.response.send_message(f"Ticket created: {channel.mention}")

@tree.command(name="ticket-close", description="Close a ticket")
async def ticket_close(interaction: discord.Interaction):
    await interaction.channel.delete()
    await interaction.response.send_message("Ticket Closed ✔")

# =====================================================================
# WELCOME EVENT
# =====================================================================

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"Welcome {member.mention} to {member.guild.name}!")

# =====================================================================
# BOT RUN
# =====================================================================

bot.run(TOKEN)
