import discord
from discord.ext import commands
from discord import app_commands

class GreetSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @app_commands.command(
        name="setgreet",
        description="Set up the greeting system."
    )
    @app_commands.describe(
        channel="The channel where greeting messages will be sent"
    )
    @commands.has_permissions(administrator=True)
    async def setup_greet(self, interaction: discord.Interaction, channel: discord.TextChannel):
        server_id = interaction.guild.id
        self.db.set_greet_channel(server_id, channel.id)
        await interaction.response.send_message(f"Greeting system set up in {channel.mention}", ephemeral=True)

    @commands.command(name="setgreet", help="Set up a greet system.", usage="#channel")
    @commands.has_permissions(administrator=True)
    async def setup_greet_prefix(self, ctx, channel: discord.TextChannel):
        server_id = ctx.guild.id
        self.db.set_greet_channel(server_id, channel.id)
        await ctx.send(f"Greeting system set up in {channel.mention}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server_id = member.guild.id
        channel_id = self.db.get_greet_channel(server_id)
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed = discord.Embed(
                    title=f"Welcome! {member.name}",
                    description=f"Welcome to {member.guild.name}!",
                    color=discord.Color(0x33ddee)
                )
                embed.set_thumbnail(url=member.avatar.url)
                embed.set_footer(text=f"{member.guild.name} has {len(member.guild.members)} members!")
                embed.timestamp = discord.utils.utcnow()
                await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GreetSystem(bot))
