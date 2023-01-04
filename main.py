"""Main class to initialize the programm"""
import os
from threading import Thread

import discord
from discord.ext import commands

import autorun
from commands.extra_features import CustomFormatter


class MCservers(commands.Bot):
    """Bot setup function"""
    def __init__(self) -> None:
        super().__init__(command_prefix = "-", intents = discord.Intents.all(), 
                         application_id = "941626533079052318")

    async def setup_hook(self) -> None:
        await self.load_extension("commandhandler")
        await bot.tree.sync(guild = discord.Object(id = 644958670353989632))

    async def on_ready(self):
        """called when the bot has connected to discord
        sets user activity and prints bot user name"""
        print(f'Logged in as: {self.user} Ready!')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                            name="-help"),
                                                            status=discord.Status.do_not_disturb)
        Thread(target=autorun.Autorun().main).start()

bot = MCservers()

def configmanager():
    """creates config if non existitent with default properties, starts bot with token requires user
     to enter token if not in config"""
    if not os.path.isfile("config.conf"):
        with open("config.conf", "w+", encoding="utf8") as conf:
            conf.write("autorunrepeat=600\nthreadlimit=250\ntoken=")
    else:
        with open("config.conf", encoding="utf8") as conf:
            for i, line in enumerate(conf):
                if line.strip().split("=")[1] == "":
                    print(f"invalid config on {line}")
                    break
                if i == 2:
                    bot.run(line.strip().split("=")[1])

configmanager()
