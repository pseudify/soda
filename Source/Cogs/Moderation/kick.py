import discord
from discord.ext import commands
from discord import app_commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(
        name="kick",
        help="Kick a user from the server.",
        usage="@user <reason>"
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str):
        await member.kick(reason=reason)
        self.db.add_infraction(member.id, ctx.author.id, reason, "kick")

        embed = discord.Embed(
            title=f"{member} has been kicked!",
            color=0x42d3e0
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Kicked by {ctx.author}")
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed)

    @app_commands.command(
        name="kick",
        description="Kick a user from the server."
    )
    @app_commands.describe(
        member="The user to kick",
        reason="The reason for the kick"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await member.kick(reason=reason)
        self.db.add_infraction(member.id, interaction.user.id, reason, "kick")

        embed = discord.Embed(
            title=f"{member} has been kicked!",
            color=0x42d3e0
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Kicked by {interaction.user}")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.send_message(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @kick_slash.error
    async def kick_slash_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Kick(bot))