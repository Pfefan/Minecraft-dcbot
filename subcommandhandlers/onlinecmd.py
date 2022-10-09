"""Module imports"""
import discord

import databasemanager


class OnlineCmd:
    """class to show all server stats for all entries in database"""
    def __init__(self) -> None:
        self.data = [] # list of servers
        self.page = 0 # page of the embed
        self.msg = ""   # message of the embed, so it can be edited

    async def showembed(self, ctx, message):
        """shows a embed based on the database"""
        self.data = databasemanager.Databasemanager().onserversget()

        if message == "reverse":
            self.data.sort(key=lambda x: int(x[2]))
        elif message is None:
            self.data.sort(key=lambda x: int(x[2]), reverse=True)

        await self.onembed(ctx)

    async def checkreaction(self, reaction, user):
        """functions to handle reactions"""
        if str(reaction.emoji) == "⬅️":
            if self.page != 0:
                self.page -= 1
                await self.updatoneembed()
                await reaction.message.remove_reaction(reaction.emoji, user)
        if str(reaction.emoji) == "➡️":
            if (self.page + 1) * 10 < len(self.data) - 1:
                self.page += 1
                await self.updatoneembed()
            await reaction.message.remove_reaction(reaction.emoji, user)

    async def onembed(self, ctx):
        """func to show embed"""
        self.page = 0
        counter = self.page * 10
        out = ""
        pagelengh = 0

        # embed for displaying info
        embed = discord.Embed(title="Servers", description=f"found {len(self.data)} servers " +
                                                    "which are online out of " +
                                                    f"{databasemanager.Databasemanager().lengh()}",
                                                    color=0x1FFF0F)
        while counter < len(self.data) and pagelengh < 10:
            out += f"{counter + 1}. IP: {self.data[counter][0]} | version: " +\
                   f"{self.data[counter][1][0:50]} | players: {self.data[counter][2]} \n"
            counter += 1
            pagelengh += 1
        embed.add_field(name=f"Page: {self.page + 1}", value=out,
                           inline=False)
        self.msg = await ctx.channel.send(embed=embed)
        await self.msg.add_reaction("⬅️")
        await self.msg.add_reaction("➡️")

    async def updatoneembed(self):
        """class to update embed on reaction"""
        out = ""
        pagelengh = 0
        counter = self.page * 10

        embededit = discord.Embed(title="Servers", description=f"found {len(self.data)} servers " +
                                                    "which are online out of " +
                                                    f"{databasemanager.Databasemanager().lengh()}",
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
