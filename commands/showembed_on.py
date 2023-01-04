"""Prints out a embed with data about servers with buttons to switch between sites"""
import asyncio

import discord
from discord.ext.commands import Paginator
from discord.ui import Button, View
from discord.ext import commands

import databasemanager


class OnEmbed:
    """class to show all server stats for all entries in database"""
    def __init__(self) -> None:
        self.data = [] # list of servers
        self.page = 0
        self.interaction = None
        self.paginator = None

    async def sortdata(self, ctx, listorder):
        """Sorts data"""
        self.data = databasemanager.Databasemanager().on_getall()

        if listorder == "reverse":
            self.data.sort(key=lambda x: int(x[2]))
        elif listorder is None:
            self.data.sort(key=lambda x: int(x[2]), reverse=True)

        await self.onembed(ctx)

    async def onembed(self, interaction):
        """Shows embed for on data"""
        self.interaction = interaction

        # Create a paginator object with a maximum page size of 1024 characters and a maximum of 2 pages
        self.paginator = commands.Paginator(max_size=1024)
        # Iterate over the tuples in the list and add them to the paginator
        for value in self.data:
            self.paginator.add_line(f"{value[0]} | {value[1]} | {value[2]}")
        # Create an embed object with a title and a color
        embed = discord.Embed(title="Online Servers", color=0x00ff00, description="A List of Online Servers")
        embed.add_field(name=f"IP{' '*10}|{' '*10}Version{' '*10}|{' '*10}Online Players", value=self.paginator.pages[self.page], inline=False)


        # add buttons to the message to create navigation buttons
        prev_button = discord.ui.Button(label="Prev", style=discord.ButtonStyle.gray, emoji="⬅️")
        next_button = discord.ui.Button(label="Next", style=discord.ButtonStyle.gray, emoji="➡️")
        enter_page_button = discord.ui.Button(label="Enter Page", style=discord.ButtonStyle.gray, emoji="🔢")

        prev_button.callback = self.next_button_callback
        next_button.callback = self.prev_button_callback

        view = View()
        view.add_item(prev_button)
        view.add_item(enter_page_button)
        view.add_item(next_button)
        
        await self.interaction.response.send_message(embed=embed, view=view)

    async def update_onembed(self):
        """updates embed for displaying diffrent pages"""
        embed = discord.Embed(title="Online Servers", color=0x00ff00, description="A List of Online Servers")
        embed.add_field(name=f"IP{' '*10}|{' '*10}Version{' '*10}|{' '*10}Online Players",
                        value=self.paginator.pages[self.page], inline=False)


        # add buttons to the message to create navigation buttons
        prev_button = discord.ui.Button(label="Prev", style=discord.ButtonStyle.gray, emoji="⬅️")
        next_button = discord.ui.Button(label="Next", style=discord.ButtonStyle.gray, emoji="➡️")
        enter_page_button = discord.ui.Button(label="Enter Page", style=discord.ButtonStyle.gray, emoji="🔢")

        next_button.callback = self.next_button_callback
        prev_button.callback = self.prev_button_callback

        view = View()
        view.add_item(prev_button)
        view.add_item(enter_page_button)
        view.add_item(next_button)
        
        await self.interaction.edit_original_response(embed=embed, view=view)
        
    
    async def next_button_callback(self, interaction):
        print("wee")
        self.page += 1
        await self.update_onembed()

    async def prev_button_callback(self, interaction):
        self.page -= 1
        await self.update_onembed()
