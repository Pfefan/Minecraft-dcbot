"""Module to list specific servers listed by proberties"""
import discord
from discord.ui import Button, View
import databasemanager


class Listserver():
    """Listserver Class"""
    def __init__(self) -> None:
        self.data = []
        self.page = 0
        self.msg = ""

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
                await self.embed(interaction) # embed for displaying info
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
                await self.embed(interaction) # embed for displaying info
            else:
                self.msg = await interaction.response.send_message("no servers were found with the given properties")

        else:
            self.msg = await interaction.response.send_message("unknown option given, options: -version, -players")


    async def embed(self, interaction):
        """embed for list func"""

        counter = self.page * 10
        out = ""
        lenghcount = 0
        embed = None

        # embed for displaying info
        embed = discord.Embed(title="Servers", description=f"found {len(self.data)} " +
                                                            "with specific properties"
                                                            , color=0xFF0000)
        while counter < len(self.data) and lenghcount < 10:
            out += f"{counter + 1}. IP: {self.data[counter][0]} | version: " +\
                   f"{self.data[counter][1][0:50]} | players: {self.data[counter][2]} \n"
            counter += 1
            lenghcount += 1
        embed.add_field(name=f"Page: {self.page + 1}", value=out,
                           inline=False)

        previousbtn = Button(label="previous", style=discord.ButtonStyle.gray, emoji="⏮️")
        nextbtn = Button(label="Next", style=discord.ButtonStyle.gray, emoji="⏭️")

        view = View()
        view.add_item(previousbtn)
        view.add_item(nextbtn)
        await interaction.response.send_message(embed=embed, view=view)


    async def updateembed(self):
        """class to update embed on reaction"""
        out = ""
        lenghcount = 0
        counter = self.page * 10

        embededit = discord.Embed(title="Servers", description=f"found {len(self.data)} " +
                                                            "with specific properties"
                                                            , color=0xFF0000)
        while(counter < len(self.data) and lenghcount < 10):
            out += f"{counter + 1}. IP: {self.data[counter][0]} | version: " +\
                   f"{self.data[counter][1][0:50]} | players: {self.data[counter][2]} \n"
            counter += 1
            lenghcount += 1
        embededit.add_field(name=f"Page: {self.page + 1}", value=out,
                            inline=False)
        await self.msg.edit(embed=embededit)
        out = None


    async def checkreaction(self, reaction, user):
        """functions to handle reactions"""
        if str(reaction.emoji) == "⏮️":
            if self.page != 0:
                self.page -= 1
                await self.updateembed()
                await reaction.message.remove_reaction(reaction.emoji, user)
        if str(reaction.emoji) == "⏭️":
            if (self.page + 1) * 10 < len(self.data) - 1:
                self.page += 1
                await self.updateembed()
            await reaction.message.remove_reaction(reaction.emoji, user)
