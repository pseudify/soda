import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(
        name="timeout",
        help="Timeout a user",
        usage="@user <duration> <reason>"
    )
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, duration: str, *, reason: str):
        duration_seconds = self.parse_duration(duration)
        if duration_seconds is None:
            await ctx.send("Invalid duration format. Use s, m, h, or d for seconds, minutes, hours, or days respectively.")
            return

        await member.timeout(timedelta(seconds=duration_seconds), reason=reason)
        self.db.add_infraction(member.id, ctx.author.id, reason, "timeout")

        embed = discord.Embed(
            title=f"{member} has been timed out!",
            color=0x42d3e0
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Duration", value=duration, inline=False)
        embed.set_footer(text=f"Timed out by {ctx.author}")
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed)

    @app_commands.command(
        name="timeout",
        description="Timeout a user temporarily."
    )
    @app_commands.describe(
        member="The user to timeout",
        duration="The duration of the timeout (s, m, h, d)",
        reason="The reason for the timeout"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout_slash(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str):
        duration_seconds = self.parse_duration(duration)
        if duration_seconds is None:
            await interaction.response.send_message("Invalid duration format. Use s, m, h, or d for seconds, minutes, hours, or days respectively.", ephemeral=True)
            return

        await member.timeout(timedelta(seconds=duration_seconds), reason=reason)
        self.db.add_infraction(member.id, interaction.user.id, reason, "timeout")

        embed = discord.Embed(
            title=f"{member} has been timed out!",
            color=0x42d3e0
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Duration", value=duration, inline=False)
        embed.set_footer(text=f"Timed out by {interaction.user}")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.send_message(embed=embed)

    def parse_duration(self, duration: str):
        try:
            unit = duration[-1]
            time = int(duration[:-1])
            if unit == 's':
                return time
            elif unit == 'm':
                return time * 60
            elif unit == 'h':
                return time * 3600
            elif unit == 'd':
                return time * 86400
            else:
                return None
        except ValueError:
            return None

    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @timeout_slash.error
    async def timeout_slash_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Timeout(bot))
