import discord
from discord.ext import commands
from discord import app_commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(
        name="ban",
        help="Ban a user from the server.",
        usage="@user <reason>"
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str):
        await member.ban(reason=reason)
        self.db.add_infraction(member.id, ctx.author.id, reason, "ban")

        embed = discord.Embed(
            title=f"{member} has been banned!",
            color=0x42d3e0
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Banned by {ctx.author}")
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed)

    @app_commands.command(
        name="ban",
        description="Ban a user from the server."
    )
    @app_commands.describe(
        member="The user to ban",
        reason="The reason for the ban"
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await member.ban(reason=reason)
        self.db.add_infraction(member.id, interaction.user.id, reason, "ban")

        embed = discord.Embed(
            title=f"{member} has been banned!",
            color=0x42d3e0
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Banned by {interaction.user}")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.send_message(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @ban_slash.error
    async def ban_slash_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ban(bot))
