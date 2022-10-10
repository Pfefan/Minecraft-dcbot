"""Module to handel playeractivity recording"""
import datetime
import itertools
import os

import discord
import matplotlib.pyplot as plt
import databasemanager


class Main:
    """Manage playeraktivites on servers"""
    def __init__(self):
        self.dbmanger = databasemanager.Databasemanager()

    async def main(self, interaction, cmd=None, proberties=None):
        """main class to control diffrent commands"""
        if cmd == "add":
            await self.add(interaction, proberties)
        elif cmd == "list":
            await self.listwatchserver(interaction)
        elif cmd == "remove":
            await self.remove(interaction, proberties)
        elif cmd == "info":
            await self.info(interaction, proberties)
        elif cmd == "opttime":
            await self.opttime(interaction, proberties)
        else:
            await interaction.response.send_message("unknown command")

    async def add(self, interaction, server_ip):
        """add a new server to the database which is gona be watched"""
        self.dbmanger.plyhistoryadd(server_ip)
        await interaction.response.send_message(f"Added {server_ip} to the database")

    async def listwatchserver(self, interaction):
        """list all servers which are being watched"""
        counter = 1
        data = self.dbmanger.plyhistoryall()
        if len(data) == 0:
            await interaction.response.send_message("No servers are being watched")
        else:
            embed = discord.Embed(title="Watching servers", description="A List " +
                                 "of servers which are watched", color=0xFFFF00)
            for i in data:
                embed.add_field(name=f"{counter}.", value=i, inline=False)
                counter += 1
            await interaction.response.send_message(embed=embed)

    async def remove(self, ctx, message):
        """remove a server from the database"""
        self.dbmanger.plyhistoryremove(message)
        await ctx.response.send_message("removed server")

    async def opttime(self, ctx, message):
        """get optimal time to join a server when the least players are online"""
        data = self.dbmanger.plyhistoryinfoget(message)
        counter = 0
        minplayers = 9999999999999
        mintimestamp = ""
        avgplayer = 0
        avgtime = []

        mindaydata = []
        daylist = [list(group) for k, group in itertools.groupby([i[2] for i in data],
                                                                 key=datetime.datetime.toordinal)]
        for day in daylist:
            for datestamp in day:
                if data[counter][0] < minplayers:
                    minplayers = data[counter][0]
                    mintimestamp = datestamp
                counter += 1
            mindaydata.append((minplayers, mintimestamp))
            minplayers = 9999999999999

        for players in mindaydata:
            avgplayer += players[0]
            avgtime.append(players[1])
        avgplayer = avgplayer / len(mindaydata)
        avgtime=datetime.datetime.strftime(datetime.datetime.fromtimestamp(sum(map(datetime.datetime.timestamp,avgtime))/len(avgtime)),"%H:%M:%S")

        embed = discord.Embed(title="Opttime", description="Most inactive server hours",
                              color=0x00fff0)
        embed.add_field(name="average: ", value=f"players:{avgplayer} | time: {avgtime}", inline=False)
        for day in mindaydata:
            embed.add_field(name=f"{day[1].strftime('%d.%m %H:%M')}", value=(day[0]), inline=True)
        await ctx.response.send_message(embed=embed)


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
            await ctx.response.send_message(file=picture)