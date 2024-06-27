import discord
from discord.ext import commands
from discord import app_commands

class ClearInfractions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.devs = self.bot.config["devs"]

    def is_dev():
        async def predicate(ctx):
            return str(ctx.author.id) in ctx.cog.devs
        return commands.check(predicate)

    @commands.command(
        name="clrinf",
        help="Clear all infractions for a user.",
        usage="@user"
    )
    @is_dev()
    async def clear_infractions(self, ctx, member: discord.Member):
        self.db.clear_infractions(member.id)
        await ctx.send(f"All infractions for {member.mention} have been cleared.")

    @app_commands.command(
        name="clrinf",
        description="Clear all infractions for a user"
    )
    @app_commands.describe(
        member="The user to clear infractions for"
    )
    @is_dev()
    async def clear_infractions_slash(self, interaction: discord.Interaction, member: discord.Member):
        self.db.clear_infractions(member.id)
        await interaction.response.send_message(f"All infractions for {member.mention} have been cleared.")

    @clear_infractions.error
    async def clear_infractions_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @clear_infractions_slash.error
    async def clear_infractions_slash_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ClearInfractions(bot))
