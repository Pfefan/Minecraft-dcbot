"""Module imports"""
import os

import discord
import matplotlib.pyplot as plt

import editdatabase


class Main:
    """Manage playeraktivites on servers"""
    def __init__(self):
        self.dbmanger = editdatabase.Databasemanager()

    async def main(self, ctx, cmd=None, message=None):
        """main class to control diffrent commands"""
        if cmd == "add":
            await self.add(ctx, message)
        elif cmd == "list":
            await self.listwatchserver(ctx)
        elif cmd == "remove":
            await self.remove(ctx, message)
        elif cmd == "info":
            await self.info(ctx, message)
        elif cmd == "opttime":
            await self.opttime(ctx, message)
        else:
            await ctx.channel.send("unknown command")

    async def add(self, ctx, message):
        """add a new server to the database which is gona be watched"""
        self.dbmanger.plyhistoryadd(message)
        await ctx.channel.send("added server")

    async def listwatchserver(self, ctx):
        """list all servers which are being watched"""
        counter = 1
        data = self.dbmanger.plyhistoryall()
        if len(data) == 0:
            await ctx.channel.send("No servers are being watched")
        else:
            embed = discord.Embed(title="Watching servers", description="A List " +
                                 "of servers which are watched", color=0xFFFF00)
            for i in data:
                embed.add_field(name=f"{counter}.", value=i, inline=False)
                counter += 1
            await ctx.channel.send(embed=embed)

    async def remove(self, ctx, message):
        """remove a server from the database"""
        self.dbmanger.plyhistoryremove(message)
        await ctx.channel.send("removed server")

    async def opttime(self, ctx, message):
        """get optimal time to join a server when the least players are online"""
        data = self.dbmanger.plyhistoryinfoget(message)
        await ctx.channel.send(min(data))


    async def info(self, ctx, message):
        """return info of a selected server"""
        data = self.dbmanger.plyhistoryinfoget(message)
        playerdata = []
        datetimedata = []

        for i in data:
            playerdata.append(i[0])
            datetimedata.append(i[2])

        fig, axis = plt.subplots(figsize=(16, 9))
        # plt.tight_layout()
        axis.plot(datetimedata, playerdata)

        axis.set(xlabel='datetime m-d H:M', ylabel='players',
            title=f'player data of {message}')
        axis.grid()

        direxist = os.path.exists("pics/")
        if not direxist:
            os.makedirs("pics/")

        fig.savefig("pics/diagramm.png")

        with open('pics/diagramm.png', 'rb') as file:
            picture = discord.File(file)
            await ctx.channel.send(file=picture)
