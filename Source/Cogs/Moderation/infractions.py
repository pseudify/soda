import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(
        name="viewinf",
        help="View a user's infractions.",
        usage="@user"
    )
    @commands.has_permissions(manage_messages=True)
    async def view_infractions(self, ctx, member: discord.Member):
        await self.send_infractions(ctx, member)

    @app_commands.command(
        name="viewinf",
        description="View a user's infractions"
    )
    @app_commands.describe(
        member="The user to view infractions for"
    )
    async def view_infractions_slash(self, interaction: discord.Interaction, member: discord.Member):
        await self.send_infractions(interaction, member)

    async def send_infractions(self, context, member: discord.Member):
        infractions = self.db.get_infractions(member.id)
        if not infractions:
            await context.send(f"{member.mention} has no infractions.") if isinstance(context, commands.Context) else await context.response.send_message(f"{member.mention} has no infractions.")
            return

        embed = discord.Embed(
            title=f"Infractions for {member}",
            color=discord.Color(0x42d3e0)
        )

        for infraction_id, moderator_id, reason, punishment_type, timestamp in infractions:
            moderator = context.guild.get_member(moderator_id)
            moderator_name = moderator.name if moderator else "Unknown"
            embed.add_field(
                name=f"Infraction ID: {infraction_id}",
                value=f"**Punishment:** {punishment_type}\n**Reason:** {reason}\n**Moderator:** {moderator_name}\n**Date:** {timestamp}",
                inline=False
            )

        await context.send(embed=embed) if isinstance(context, commands.Context) else await context.response.send_message(embed=embed)

    @view_infractions.error
    async def view_infractions_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @view_infractions_slash.error
    async def view_infractions_slash_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
