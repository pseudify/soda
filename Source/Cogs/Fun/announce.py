import discord
from discord.ext import commands
from discord import app_commands

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="announce",
        help="Announce a message in a specified channel",
        usage="#channel <message>"
    )
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, channel: discord.TextChannel, *, message: str):
        embed = discord.Embed(
            description=message,
            color=0x42d3e0
        )
        embed.set_footer(text=f"Announcement by {ctx.author}")
        embed.timestamp = discord.utils.utcnow()
        await channel.send(embed=embed)
        await ctx.send(f"Announcement sent in {channel.mention}")

    @app_commands.command(
        name="announce",
        description="Announce a message in a specified channel"
    )
    @app_commands.describe(
        channel="The channel to send the announcement in",
        message="The announcement message"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def announce_slash(self, interaction: discord.Interaction, channel: discord.TextChannel, message: str):
        embed = discord.Embed(
            description=message,
            color=0x42d3e0
        )
        embed.set_footer(text=f"Announcement by {interaction.user}")
        embed.timestamp = discord.utils.utcnow()
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Announcement sent in {channel.mention}", ephemeral=True)

    @announce.error
    async def announce_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send("The specified channel was not found.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @announce_slash.error
    async def announce_slash_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        elif isinstance(error, app_commands.errors.ChannelNotFound):
            await interaction.response.send_message("The specified channel was not found.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Announce(bot))
