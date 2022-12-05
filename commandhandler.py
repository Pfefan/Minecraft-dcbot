"""Main command handler to handel slash commands"""
import discord
from discord import app_commands
from discord.ext import commands

import autorun
import commands.details as details
import commands.serverlookup_on as serverlookup_on
import commands.showembed_on as showembed_on
import subcommandhandlers.list_on as liston
import subcommandhandlers.playeraktivitycmd as playeraktivitycmd


class Commandhandler(commands.Cog):
    """discord commands"""

    def __init__(self, bot: commands.Bot):
        """init func"""
        self.bot = bot
        self.onlookup = serverlookup_on.Lookup()
        self.onlinecmd = showembed_on.OnEmbed()
        self.detailscmd = details.Details()
        self.watchserver = playeraktivitycmd.Main()
        self.autorun = autorun.Autorun()
        self.listcmd = liston.Listserver()

    @app_commands.command(
        name = "online",
        description = "Displays info about online servers")

    async def online (self, interaction: discord.Interaction, listorder:str = None):
        """command to get servers with players online"""
        await self.onlinecmd.sortdata(interaction, listorder)

    @app_commands.command(
        name = "onlinelookup",
        description = "Checks status of stored Servers in database")

    async def onlinelookup (self, interaction: discord.Interaction):
        """goes through all servers and checks if they are online"""
        await interaction.response.send_message("Looking for online Servers! Will take about 10 minutes")
        await self.onlookup.serverlookup(interaction)

    @app_commands.command(
        name = "details",
        description = "Gets details of a specifc server")

    async def details(self, interaction: discord.Interaction, serverip:str):
        """command to get details about a server"""
        await self.detailscmd.main(interaction, serverip)

    @app_commands.command(
        name = "watch",
        description = "Logging user count on server")

    async def watch(self, interaction: discord.Interaction, command:str, extra_properties:str = None):
        """playeractivity on a server"""
        await self.watchserver.main(interaction, command, extra_properties)

    @app_commands.command(
        name = "autorunconfig",
        description = "Change autolookup interval in minutes")

    async def autorunconfig(self, interaction: discord.Interaction, repeattime:str):
        """changes autoconfig time in minutes"""
        await self.autorun.changerepeattime(interaction, repeattime)

    @app_commands.command(
        name = "list",
        description = "Lists servers with specific properties")

    async def list(self, interaction: discord.Interaction, listmode:str, sortproperties:str):
        """command to List specific servers"""
        await self.listcmd.main(interaction, listmode, sortproperties)

async def setup(bot: commands.Bot) -> None:
    """Cogs setup func"""
    await bot.add_cog(
        Commandhandler(bot),
        guilds= [discord.Object(id = 644958670353989632)]
    )
