import discord
from discord.ext import commands
import json
import re
import os

DATA_FILE = "data/automod.json"

# Default config with English + Hinglish abusive words
default_config = {
    "bad_words": [
        # English abusive words
        "fuck", "shit", "bitch", "asshole", "bastard", "dick", "piss", "crap", "slut", "whore", "cunt", "damn",
        "motherfucker", "nigga", "nigger",
        # Hinglish/Indian abusive words
        "chutiya", "bhosdike", "madarchod", "lund", "gandu", "randi", "harami", "bhainschod", "bhenchod", "chodu"
    ],
    "block_invites": True,
    "spam_limit": 5
}

# Create the JSON file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump(default_config, f, indent=4)

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(DATA_FILE, "r") as f:
            self.config = json.load(f)
        self.user_messages = {}  # For spam detection

    # --- Bad Word, Invite & Spam Blocking ---
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Load config
        with open(DATA_FILE, "r") as f:
            self.config = json.load(f)

        # Check for bad words (English + Hinglish)
        for word in self.config.get("bad_words", []):
            if word.lower() in message.content.lower():
                await message.delete()
                await message.channel.send(
                    f"❌ {message.author.mention}, your message contains abusive words! | Powered by JC Cheats",
                    delete_after=5
                )
                return

        # Check for Discord invite links
        if self.config.get("block_invites", True):
            if re.search(r"(?:https?://)?discord(?:\.gg|app\.com/invite)/[^\s]+", message.content):
                await message.delete()
                await message.channel.send(
                    f"❌ {message.author.mention}, Discord invite links are not allowed! | Powered by JC Cheats",
                    delete_after=5
                )
                return

        # Spam detection (5 messages in 10 seconds)
        user_id = message.author.id
        self.user_messages.setdefault(user_id, [])
        self.user_messages[user_id].append(message.created_at)

        # Remove old messages
        self.user_messages[user_id] = [t for t in self.user_messages[user_id] if (message.created_at - t).total_seconds() <= 10]

        if len(self.user_messages[user_id]) > self.config.get("spam_limit",5):
            await message.channel.send(
                f"⚠️ {message.author.mention}, you are spamming! | Powered by JC Cheats",
                delete_after=5
            )
            try:
                await message.author.timeout(duration=10, reason="Spamming")
            except:
                pass
            self.user_messages[user_id] = []

def setup(bot):
    bot.add_cog(Automod(bot))
