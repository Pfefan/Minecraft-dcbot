"""Prints out a embed with data about servers with buttons to switch between sites"""
import discord

import databasemanager


class OnEmbed:
    """class to show all server stats for all entries in database"""
    def __init__(self) -> None:
        self.data = [] # list of servers
        self.page = 0 # page of the embed
        self.msg = ""   # message of the embed, so it can be edited

    async def sortdata(self, ctx, listorder):
        """Sorts data"""
        self.data = databasemanager.Databasemanager().on_getall()

        if listorder == "reverse":
            self.data.sort(key=lambda x: int(x[2]))
        elif listorder is None:
            self.data.sort(key=lambda x: int(x[2]), reverse=True)

        await self.onembed(ctx)

    async def onembed(self, interaction):
        """Shows data in embed form"""
        self.page = 0
        counter = self.page * 10
        out = ""
        pagelengh = 0

        # embed for displaying info
        embed = discord.Embed(title="Servers", description=f"found {len(self.data)} servers " +
                                                    "which are online out of " +
                                                    f"{databasemanager.Databasemanager().default_lengh()}",
                                                    color=0x1FFF0F)
        while counter < len(self.data) and pagelengh < 10:
            out += f"{counter + 1}. IP: {self.data[counter][0]} | version: " +\
                   f"{self.data[counter][1][0:50]} | players: {self.data[counter][2]} \n"
            counter += 1
            pagelengh += 1
        embed.add_field(name=f"Page: {self.page + 1}", value=out,
                           inline=False)
        self.msg = await interaction.response.send_message(embed=embed)

    async def updatoneembed(self):
        """class to update embed on reaction"""
        out = ""
        pagelengh = 0
        counter = self.page * 10

        embededit = discord.Embed(title="Servers", description=f"found {len(self.data)} servers " +
                                                    "which are online out of " +
                                                    f"{databasemanager.Databasemanager().default_lengh()}",
                                                    color=0x1FFF0F)
        while(counter < len(self.data) and pagelengh < 10):
            out += f"{counter + 1}. IP: {self.data[counter][0]} | version: " +\
                   f"{self.data[counter][1][0:50]} | players: {self.data[counter][2]} \n"
            counter += 1
            pagelengh += 1
        embededit.add_field(name=f"Page: {self.page + 1}", value=out,
                            inline=False)
        await self.msg.edit(embed=embededit)
        out = None
