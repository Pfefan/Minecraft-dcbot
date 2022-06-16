import editdatabase
import discord

class Main:
    """Manage playeraktivies on servers"""
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
                                 "of servers which are watched", color=0xFFA500)
            for i in data:
                embed.add_field(name=f"{counter}.", value=i, inline=False)
                counter += 1
            await ctx.channel.send(embed=embed)

    async def remove(self, ctx, message):
        """remove a server from the database"""
        self.dbmanger.plyhistoryremove(message)
        await ctx.channel.send("removed server")
        

    async def details(self, message, ctx):
        """print all player activities which are logged in the database"""
        pass
