"""Module to list specific servers listed by proberties"""
from msilib.schema import Feature
import discord
from discord.ui import Button, View
import databasemanager
from commands.extra_features import Features


class Listserver():
    """Listserver Class"""
    def __init__(self) -> None:
        self.data = []
        self.page = 0

    async def main(self, interaction, option, properties):
        """search for server with specific properties"""
        self.data.clear()
        self.page = 0
        if self.msg != None and self.msg != "":
            await self.msg.delete()  #deletes last message

        if option == "version":
            serverlist = databasemanager.Databasemanager().onserversget()

            for server in serverlist:
                if server[1].find(properties) != -1:
                    self.data.append(server)

            if len(self.data) > 0:
                await self.output(interaction) # embed for displaying info
            else:
                self.msg = await interaction.response.send_message("no servers were found with the given properties")

        elif option == "players":
            serverlist = databasemanager.Databasemanager().onserversget()
            if len(properties.split("-")) > 1:
                maxplayers = int(properties.split("-")[1]) # splits up max min amount
                minplayers = int(properties.split("-")[0])
                for server in serverlist: # search through every entriy in the database
                    if server[2] >= int(minplayers) and server[2] <= int(maxplayers):
                        self.data.append(server)
            else:
                for server in serverlist: # search through every entriy in the database
                    if server[2] == int(properties):
                        self.data.append(server)

            if len(self.data) > 0:
                await self.output(interaction) # embed for displaying info
            else:
                self.msg = await interaction.response.send_message("no servers were found with the given properties")

        else:
            self.msg = await interaction.response.send_message("unknown option given, options: -version, -players")


    async def output(self, interaction):
        """embed for list func"""

        counter = self.page * 10
        tabledata = []
        maxlimit = 0

        while counter < len(self.data) and maxlimit < 10:
            tabledata.append((self.data[counter][0], self.data[counter][1], self.data[counter][2]))
            counter += 1
            maxlimit += 1

        previousbtn = Button(label="previous", style=discord.ButtonStyle.gray, emoji="⏮️")
        nextbtn = Button(label="Next", style=discord.ButtonStyle.gray, emoji="⏭️")

        previousbtn.callback = self.previousbtn_callback
        nextbtn.callback = self.nextbtn_callback

        view = View()
        view.add_item(previousbtn)
        view.add_item(nextbtn)
        
        await interaction.response.send_message(Features.tablegen(("Hostname", "Version", "players"), tabledata), view=view)


    async def onpagechange(self, interaction):
        """class to update embed on reaction"""
        counter = self.page * 10
        tabledata = []
        maxlimit = 0
        await self.msg.delete()
        while counter < len(self.data) and maxlimit < 10:
            tabledata.append((self.data[counter][0], self.data[counter][1], self.data[counter][2]))
            counter += 1
            maxlimit += 1

        previousbtn = Button(label="previous", style=discord.ButtonStyle.gray, emoji="⏮️")
        nextbtn = Button(label="Next", style=discord.ButtonStyle.gray, emoji="⏭️")

        previousbtn.callback = self.previousbtn_callback
        nextbtn.callback = self.nextbtn_callback

        view = View()
        view.add_item(previousbtn)
        view.add_item(nextbtn)
        
        await interaction.response.send_message(Features.tablegen(("Hostname", "Version", "players"), tabledata), view=view)

    async def nextbtn_callback(self, interaction):
            if (self.page + 1) * 10 < len(self.data) - 1:
                self.page += 1
                await self.onpagechange(interaction)

    async def previousbtn_callback(self, interaction):
        if self.page != 0:
            self.page -= 1
            await self.onpagechange(interaction)
