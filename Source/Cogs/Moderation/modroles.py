import discord
from discord.ext import commands
from discord import app_commands

class ModRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(
        name="addmodroles",
        help="Add a role to the list of mod roles",
        usage="@role"
    )
    @commands.has_permissions(administrator=True)
    async def add_mod_role(self, ctx, role: discord.Role):
        self.db.add_mod_role(ctx.guild.id, role.id)
        embed = discord.Embed(
            description=f"Added {role.mention} to the mod roles list for {ctx.guild.name}.",
            color=0x42d3e0
        )
        await ctx.send(embed=embed)

    @app_commands.command(
        name="addmodroles",
        description="Add a role to the list of mod roles"
    )
    @app_commands.describe(
        role="The role to add to the list of mod roles"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def add_mod_role_slash(self, interaction: discord.Interaction, role: discord.Role):
        self.db.add_mod_role(interaction.guild.id, role.id)
        embed = discord.Embed(
            description=f"Added {role.mention} to the mod roles list for {interaction.guild.name}.",
            color=0x42d3e0
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.command(
        name="viewmodroles",
        help="View the list of mod roles"
    )
    @commands.has_permissions(administrator=True)
    async def view_mod_roles(self, ctx):
        roles = self.db.get_mod_roles(ctx.guild.id)
        if roles:
            role_mentions = [ctx.guild.get_role(role_id).mention for role_id in roles if ctx.guild.get_role(role_id)]
            embed = discord.Embed(
                title=f"Mod Roles for {ctx.guild.name}",
                description=", ".join(role_mentions),
                color=0x42d3e0
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No mod roles have been set.")

    @app_commands.command(
        name="viewmodroles",
        description="View the list of mod roles"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def view_mod_roles_slash(self, interaction: discord.Interaction):
        roles = self.db.get_mod_roles(interaction.guild.id)
        if roles:
            role_mentions = [interaction.guild.get_role(role_id).mention for role_id in roles if interaction.guild.get_role(role_id)]
            embed = discord.Embed(
                title=f"Mod Roles for {interaction.guild.name}",
                description=", ".join(role_mentions),
                color=0x42d3e0
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("No mod roles have been set.", ephemeral=True)

    @commands.command(
        name="delmodroles",
        help="Remove a role from the list of mod roles",
        usage="@role"
    )
    @commands.has_permissions(administrator=True)
    async def del_mod_role(self, ctx, role: discord.Role):
        self.db.remove_mod_role(ctx.guild.id, role.id)
        embed = discord.Embed(
            description=f"Removed {role.mention} from the mod roles list for {ctx.guild.name}.",
            color=0x42d3e0
        )
        await ctx.send(embed=embed)

    @app_commands.command(
        name="delmodroles",
        description="Remove a role from the list of mod roles"
    )
    @app_commands.describe(
        role="The role to remove from the list of mod roles"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def del_mod_role_slash(self, interaction: discord.Interaction, role: discord.Role):
        self.db.remove_mod_role(interaction.guild.id, role.id)
        embed = discord.Embed(
            description=f"Removed {role.mention} from the mod roles list for {interaction.guild.name}.",
            color=0x42d3e0
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @add_mod_role.error
    @view_mod_roles.error
    @del_mod_role.error
    async def mod_role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please mention a valid role.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @add_mod_role_slash.error
    @view_mod_roles_slash.error
    @del_mod_role_slash.error
    async def mod_role_slash_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        elif isinstance(error, app_commands.errors.BadArgument):
            await interaction.response.send_message("Please mention a valid role.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModRoles(bot))
