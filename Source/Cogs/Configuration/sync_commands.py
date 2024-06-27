import discord
from discord.ext import commands
import json

class SyncCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config.json') as config_file:
            self.config = json.load(config_file)
        self.devs = self.config["devs"]

    def dev_only():
        async def predicate(ctx):
            if not ctx.command.extras.get("DevOnly", False):
                return True
            if str(ctx.author.id) not in ctx.cog.devs:
                raise commands.CheckFailure("You do not have permission to use this command.")
            return True
        return commands.check(predicate)

    @commands.command(name="sync", help="Sync the command tree with Discord.", usage="", extras={"DevOnly": True})
    @dev_only()
    async def sync_commands(self, ctx):
        try:
            await self.bot.tree.sync()
            await ctx.send("Command tree synced successfully.")
        except Exception as e:
            await ctx.send(f"An error occurred while syncing commands: {e}")

async def setup(bot):
    await bot.add_cog(SyncCommands(bot))
