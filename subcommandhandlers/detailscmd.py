"""Module imports"""

import os
import urllib

import discord
from mcstatus import JavaServer

import commands.extra_features as extra_features


class Details():
    """Details cmd class"""
    def __init__(self) -> None:
        pass

    async def main(self, interaction, server_ip):
        """gets info about a specific server"""
        try:
            server = JavaServer.lookup(server_ip)
            await self.embed(interaction, server, server_ip)
            print(f"successfully got details from '{server_ip}'")
        except IOError:
            try:
                if len(server_ip.split(":")) == 2:
                    await interaction.response.send_message("server was not reachable")
                    print(f"failed to get details from {server_ip}")
                    return
                server = JavaServer.lookup(server_ip + ":25565")
                await self.embed(interaction, server, server_ip)
                print(f"successfully got details from '{server_ip}'")
            except IOError:
                await interaction.response.send_message("server was not reachable")
                print(f"failed to get details from {server_ip}")

    async def embed(self, interaction, server, hostname):
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
                           value=extra_features.Features().getplayernames(server),
                           inline=False)
        embed.add_field(name="Geolocation", value=extra_features.Features().geolocation(hostname),
                           inline=False)
        embed.set_image(url='attachment://details.png')
        if img_data is not None:
            await interaction.response.send_message(embed=embed, file=file)
        else:
            await interaction.response.send_message(embed=embed)
