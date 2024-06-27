import discord
from discord.ext import commands
from discord import app_commands

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(
        name="warn",
        help="Warn a user",
        usage="@user <reason>"
    )
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        self.db.add_infraction(member.id, ctx.author.id, reason, "warn")
        embed = discord.Embed(
            title=f"{member} was warned!",
            color=0x42d3e0
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @app_commands.command(
        name="warn",
        description="Give a user a warning."
    )
    @app_commands.describe(
        member="The user to warn",
        reason="The reason for the warning"
    )
    async def warn_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        # Custom permission check
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        
        self.db.add_infraction(member.id, interaction.user.id, reason, "warn")
        embed = discord.Embed(
            title=f"{member} was warned!",
            color=0x42d3e0
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @warn_slash.error
    async def warn_slash_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Warn(bot))
