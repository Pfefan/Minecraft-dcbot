"""Module to handel command inputs from user to redirect to functions"""
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
        self.cmdlist = ["add", "remove", "watched", "data", "lowest-activity", "help"]

    async def main(self, interaction, cmd=None, proberties=None):
        """main class to control diffrent commands"""
        if cmd == self.cmdlist[0]:
            await self.add_watchserver(interaction, proberties)
        elif cmd == self.cmdlist[1]:
            await self.remove_watchedserver(interaction, proberties)
        elif cmd == self.cmdlist[2]:
            await self.list_watchedservers(interaction)
        elif cmd == self.cmdlist[3]:
            await self.info(interaction, proberties)
        elif cmd == self.cmdlist[4]:
            await self.low_activity(interaction, proberties)
        elif cmd == self.cmdlist[5]:
            await interaction.response.send_message(f"available commands are: {', '.join(self.cmdlist)}")
        else:
            await interaction.response.send_message("unknown command")

    async def add_watchserver(self, interaction, server_ip):
        """add a new server to the database which is gona be watched"""
        self.dbmanger.watch_additem(server_ip)
        await interaction.response.send_message(f"Added {server_ip} to the database")

    async def remove_watchedserver(self, ctx, message):
        """Removes a watched server from the database"""
        self.dbmanger.watch_removebyid(message)
        await ctx.response.send_message("removed server")

    async def list_watchedservers(self, interaction):
        """list all servers which are being watched"""
        counter = 1
        data = self.dbmanger.watch_getall()
        if len(data) == 0:
            await interaction.response.send_message("No servers are being watched")
        else:
            embed = discord.Embed(title="Watching servers", description="A List " +
                                 "of servers which are watched", color=0xFFFF00)
            for i in data:
                embed.add_field(name=f"{counter}.", value=i, inline=False)
                counter += 1
            await interaction.response.send_message(embed=embed)

    async def info(self, ctx, message):
        """return info of a selected server"""
        data = self.dbmanger.watch_getdata(message)
        playerdata = []
        datetimedata = []

        for i in data:
            playerdata.append(i[0])
            datetimedata.append(i[2])

        fig, axis = plt.subplots(figsize=(16, 9))
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

    async def low_activity(self, ctx, message):
        """Gets lowest player activity of each day and the average off all the data"""
        data = self.dbmanger.watch_getdata(message)
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
