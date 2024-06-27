import discord
from discord.ext import commands
from discord import app_commands
import random

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree

    def remove_existing_command(self, name: str):
        existing_command = discord.utils.get(self.tree.get_commands(), name=name)
        if existing_command:
            self.tree.remove_command(existing_command.name, type=discord.app_commands.CommandType.chat_input)

    @commands.command()
    async def ping(self, ctx):
        await self.send_ping_embed(ctx)

    @app_commands.command(name="ping", description="Ping command")
    async def ping_slash(self, interaction: discord.Interaction):
        await self.send_ping_embed(interaction)

    async def send_ping_embed(self, context):

        footer_options = [

            "Did you hear the beat to mario there?",
            "Powered by Discord.py",
            "Latency is just a number"
        ]

        footer_text = random.choice(footer_options)

        embed = discord.Embed(
            title = "Pong!",
            color = discord.Color(0x42d3e0)
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=footer_text)
        embed.add_field(
            name = "Ping: ",
            value = f"{round(self.bot.latency * 1000)} ms"
        )
        

        if isinstance(context, commands.Context):
            await context.send(embed=embed)
        elif isinstance(context, discord.Interaction):
            await context.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(PingCog(bot))