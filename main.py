"""module import"""
from threading import Thread

import discord
from discord.ext import commands

import autorun

class MCservers(commands.Bot):
    """Discord Bot setup function"""
    def __init__(self) -> None:
        super().__init__(command_prefix = "-", intents = discord.Intents.all(), application_id = "941626533079052318")
        Thread(target=autorun.Autorun().main).start() #starting autorun thread to automaticly execute tasks

    async def setup_hook(self) -> None:
        await self.load_extension("commandhandler")
        await bot.tree.sync(guild = discord.Object(id = 644958670353989632))

    async def on_ready(self):
        """func when the bots has loaded and is online"""

        print(f'Logged in as: {self.user} Ready!')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                            name="-help"),
                                                            status=discord.Status.do_not_disturb)

    async def on_reaction_add(self, reaction, user):
        """func to check for reaction add"""
        if user != self.user:
            await self.cogs["Commandhandler"].on_reaction(reaction, user)

bot = MCservers()
bot.run(open("token.txt", encoding="utf8").readline())
