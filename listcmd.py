"""Module imports"""
import discord
import editdatabase


class Listserver():
    """Listserver Class"""
    def __init__(self) -> None:
        self.data = []
        self.page = 0
        self.msg = ""

    async def main(self, ctx, option, properties):
        """search for server with specific properties"""
        self.data.clear()
        self.page = 0
        if self.msg != None and self.msg != "":
            await self.msg.delete()  #deletes last message

        if option == "version":
            self.data = await self.getversion(properties)

            if len(self.data) > 0:
                await self.embed(ctx) # embed for displaying info
            else:
                self.msg = await ctx.channel.send("no servers were found with the given properties")

        elif option == "players":
            self.data = await self.getplayers(properties)

            if len(self.data) > 0:
                await self.embed(ctx) # embed for displaying info
            else:
                self.msg = await ctx.channel.send("no servers were found with the given properties")

        else:
            self.msg = await ctx.channel.send("unknown option given, options: -version, -players")

    async def getplayers(self, properties):
        """gets servers with specific player numbers"""
        serverlist = editdatabase.Databasemanager().onserversget()
        data = []
        if len(properties.split("-")) > 1:
            maxplayers = int(properties.split("-")[1]) # splits up max min amount
            minplayers = int(properties.split("-")[0])
            for server in serverlist: # search through every entriy in the database
                if server[2] >= int(minplayers) and server[2] <= int(maxplayers):
                    data.append(server)
        else:
            for server in serverlist: # search through every entriy in the database
                if server[2] == int(properties):
                    data.append(server)
        return data

    async def getversion(self, properties):
        """gets servers with a certain version"""
        serverlist = editdatabase.Databasemanager().onserversget()

        data = []
        for server in serverlist:
            if server[1].find(properties) != -1:
                data.append(server)
        return data


    async def embed(self, ctx):
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
        self.msg = await ctx.channel.send(embed=embed)

        await self.msg.add_reaction("⏮️")
        await self.msg.add_reaction("⏭️")


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
