"""module imports"""
from discord.ext import commands

import onlineserverlookup
import detailscmd
import listcmd
import onlinecmd
import playeraktivitycmd


class DCcmd(commands.Cog):
    """discord commands"""
 
    def __init__(self, client):
        """init func"""
        self.client = client
        self.onlookup = onlineserverlookup.Lookup()
        self.onlinecmd = onlinecmd.OnlineCmd()
        self.detailscmd = detailscmd.Details()
        self.listcmd = listcmd.Listserver()
        self.watch = playeraktivitycmd.Main()

    @commands.command()
    async def onlinelookup (self, ctx):
        """command to get servers with players online"""
        await self.onlookup.onlinecmd(ctx)

    @commands.command()
    async def online (self, ctx, message=None):
        """command to get servers with players online"""
        await self.onlinecmd.showembed(ctx, message)

    @commands.command()
    async def details(self, ctx, message=None):
        """command to get details about a server"""
        await self.detailscmd.main(ctx, message)

    @commands.command()
    async def watch(self, ctx, cmd=None, message=None):
        """command to get details about a server"""
        await self.watch.main(ctx, cmd, message)

    @commands.command()
    async def list(self, ctx, message=None, properties=None):
        """command to List specific servers"""
        await self.listcmd.main(ctx, message, properties)

    async def on_reaction(self, reaction, user):
        """on reaction"""
        if str(reaction.emoji) == "⬅️" or str(reaction.emoji) == "➡️":
            await self.onlinecmd.checkreaction(reaction, user)
        elif str(reaction.emoji) == "⏮️" or str(reaction.emoji) == "⏭️":
            await self.listcmd.checkreaction(reaction, user)

def setup(client):
    """setup"""
    client.add_cog(DCcmd(client))
