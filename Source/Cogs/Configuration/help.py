import discord
from discord.ext import commands
from discord.ui import View, Button
import json

class HelpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config.json') as config_file:
            self.config = json.load(config_file)
        self.devs = self.config["devs"]

    @commands.command(name="help", help = "Get a list of my commands.")
    async def help_command(self, ctx):
        embeds = self.create_help_embeds(ctx.author.id)
        paginator = Paginator(embeds)
        view = paginator.get_view()
        await ctx.send(embed=paginator.current_page, view=view)

    def create_help_embeds(self, author_id):
        embeds = []
        commands_per_page = 5
        all_commands = [cmd for cmd in self.bot.commands if not cmd.extras.get("DevOnly", False) or str(author_id) in self.devs]
        for i in range(0, len(all_commands), commands_per_page):
            embed = discord.Embed(
                title="Help Menu",
                description="List of available commands",
                color=discord.Color(0x42d3e0)
            )
            for cmd in all_commands[i:i + commands_per_page]:
                usage = f"{self.bot.command_prefix}{cmd.name} {cmd.usage}" if cmd.usage else f"{self.bot.command_prefix}{cmd.name}"
                embed.add_field(
                    name=usage,
                    value=cmd.help or "No description",
                    inline=False
                )
            embeds.append(embed)
        return embeds

class Paginator:
    def __init__(self, pages):
        self.pages = pages
        self.current_index = 0

    @property
    def current_page(self):
        return self.pages[self.current_index]

    def get_view(self):
        view = View()
        prev_button = Button(label="<", style=discord.ButtonStyle.primary, disabled=self.current_index == 0)
        next_button = Button(label=">", style=discord.ButtonStyle.primary, disabled=self.current_index == len(self.pages) - 1)

        prev_button.callback = self.previous_page
        next_button.callback = self.next_page

        view.add_item(prev_button)
        view.add_item(next_button)
        return view

    async def previous_page(self, interaction: discord.Interaction):
        self.current_index -= 1
        await interaction.response.edit_message(embed=self.current_page, view=self.get_view())

    async def next_page(self, interaction: discord.Interaction):
        self.current_index += 1
        await interaction.response.edit_message(embed=self.current_page, view=self.get_view())

async def setup(bot):
    await bot.add_cog(HelpMenu(bot))
