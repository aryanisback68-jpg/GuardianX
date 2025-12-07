import discord
from discord.ext import commands
from discord.ui import Button, View

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- Setup ticket message ---
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticketsetup(self, ctx):
        embed = discord.Embed(
            title="Support Ticket",
            description="Click the button below to create a ticket!",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Powered by JC Cheats")

        button = Button(label="Create Ticket", style=discord.ButtonStyle.green, emoji="🎫")

        async def button_callback(interaction):
            # Create a new ticket channel
            guild = ctx.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            ticket_channel = await guild.create_text_channel(
                name=f"ticket-{interaction.user.name}",
                overwrites=overwrites,
                reason="Ticket Created"
            )
            await interaction.response.send_message(
                f"✅ Your ticket has been created: {ticket_channel.mention} | Powered by JC Cheats",
                ephemeral=True
            )
            await ticket_channel.send(
                f"Hello {interaction.user.mention}, a staff member will be with you shortly! | Powered by JC Cheats"
            )

        button.callback = button_callback
        view = View()
        view.add_item(button)
        await ctx.send(embed=embed, view=view)

    # --- Close ticket command ---
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def closeticket(self, ctx):
        if ctx.channel.name.startswith("ticket-"):
            await ctx.send("🔒 Closing ticket in 5 seconds... | Powered by JC Cheats")
            await discord.utils.sleep_until(discord.utils.utcnow() + discord.timedelta(seconds=5))
            await ctx.channel.delete(reason="Ticket Closed")
        else:
            await ctx.send("❌ This is not a ticket channel! | Powered by JC Cheats")

def setup(bot):
    bot.add_cog(Ticket(bot))
