import discord
from discord.ext import commands
from discord import app_commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="purge",
        help="Purge a specified number of messages (max 50)",
        usage="<number of messages>"
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, num_messages: int):
        if num_messages > 50:
            await ctx.send("You can only purge up to 50 messages at a time.")
            return

        deleted = await ctx.channel.purge(limit=num_messages + 1)  # Including the command message itself

        embed = discord.Embed(
            description=f"Deleted {len(deleted) - 1} messages.",
            color=0x42d3e0
        )
        embed.set_footer(text=f"Purged by {ctx.author}")
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed, delete_after=5)

    @app_commands.command(
        name="purge",
        description="Purge a specified number of messages (max 50)"
    )
    @app_commands.describe(
        num_messages="The number of messages to purge"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge_slash(self, interaction: discord.Interaction, num_messages: int):
        if num_messages > 50:
            await interaction.response.send_message("You can only purge up to 50 messages at a time.", ephemeral=True)
            return

        deleted = await interaction.channel.purge(limit=num_messages + 1)  # Including the command message itself

        embed = discord.Embed(
            description=f"Deleted {len(deleted) - 1} messages.",
            color=0x42d3e0
        )
        embed.set_footer(text=f"Purged by {interaction.user}")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid number of messages to purge.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @purge_slash.error
    async def purge_slash_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        elif isinstance(error, app_commands.errors.BadArgument):
            await interaction.response.send_message("Please provide a valid number of messages to purge.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Purge(bot))
