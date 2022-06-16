"""module import"""
from threading import Thread

import discord
from discord.ext import commands

import authenticator
import autorun

cogs = [authenticator]

client = commands.Bot(command_prefix='-')
Thread(target=autorun.Autorun().main).start() #starting autorun thread to automaticly execute tasks
@client.event
async def on_ready():
    """func when the bots has loaded and is online"""

    print('Logged in as: ' + client.user.name)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                           name="-help"),
                                                           status=discord.Status.do_not_disturb)
    print('Ready!\n')

@client.event
async def on_reaction_add(reaction, user):
    """func to check for reaction add"""
    if user != client.user:
        await client.cogs["DCcmd"].on_reaction(reaction, user)

for i, item in enumerate(cogs):
    cogs[i].setup(client)

client.run(open("token.txt", encoding="utf8").readline())
