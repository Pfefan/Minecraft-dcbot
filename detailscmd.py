"""Module imports"""

import os
import urllib

import discord
from mcstatus import JavaServer

import databasecmd


class Details():
    """Details cmd class"""
    def __init__(self) -> None:
        pass

    async def main(self, ctx, message):
        """gets info about a specific server"""
        debugmsg = await ctx.channel.send("trying to get info about the server")
        try:
            server = JavaServer.lookup(message)
            await self.embed(ctx, server, message)
            await debugmsg.delete()
            print(f"successfully got details from '{message}'")
        except IOError:
            try:
                if len(message.split(":")) == 2:
                    await debugmsg.edit(content="server was not reachable")
                    print(f"failed to get details from {message}")
                    return
                server = JavaServer.lookup(message + ":25565")
                await self.embed(ctx, server, message)
                await debugmsg.delete()
                print(f"successfully got details from '{message}'")
            except IOError:
                await debugmsg.edit(content="server was not reachable")
                print(f"failed to get details from {message}")

    async def embed(self, ctx, server, hostname):
        """embed for details command"""
        status = server.status()
        path = "pics/details.png"
        # gets the favicon of the minecraft server
        img_data = status.favicon
        if img_data is not None:
            response = urllib.request.urlopen(img_data)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open('pics/details.png', 'wb') as file:
                file.write(response.file.read())
                file = discord.File('pics/details.png', filename="details.png")

        # embed for displaying infos
        embed = discord.Embed(title="Details about a Server", description="motd: " +
                                 status.description, color=0xFFA500)
        embed.add_field(name="ip", value=hostname, inline=True)
        embed.add_field(name="Latency in ms", value=status.latency,
                    inline=True)
        embed.add_field(name="version", value=status.version.name,
                           inline=False)
        embed.add_field(name=f"Players online ({status.players.online})",
                           value=databasecmd.CMD().getplayernames(server),
                           inline=False)
        embed.add_field(name="Geolocation", value=databasecmd.CMD().geolocation(hostname),
                           inline=False)
        embed.set_image(url='attachment://details.png')
        if img_data is not None:
            await ctx.channel.send(embed=embed, file=file)
        else:
            await ctx.channel.send(embed=embed)
