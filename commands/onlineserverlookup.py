"""Module impots"""
import time
from threading import Thread

import databasemanager
import commands.serverlookup as serverlookup

class Lookup():
    """class to automaticly ping all servers in the database"""
    def __init__(self) -> None:
        self.data = []
        self.threadcounter = 0

    async def onlinecmd(self, ctx):
        """class to search through the hole database for servers which are online"""
        self.data.clear()
        threadlengh = 10
        adresses = databasemanager.Databasemanager().all()
        outadresses = []
        ping_threads = []

        await ctx.channel.send("Searching for online servers...")
        for adress in adresses:
            while self.threadcounter > 200:
                time.sleep(0.1)
            outadresses.append(adress)
            if len(outadresses) >= threadlengh:
                lookup = serverlookup.Lookup(threadlengh, outadresses.copy(),
                                           self)
                pingthread = Thread(target=lookup.main)
                ping_threads.append(pingthread)
                pingthread.start()
                self.threadcounter += 1
                outadresses.clear()

        for pingthread in ping_threads:
            pingthread.join()

        await ctx.channel.send(f"found {len(self.data)} servers with players online " +
                f"out of {databasemanager.Databasemanager().lengh()}")
        print(f"found {len(self.data)} servers with players online " +
                f"out of {databasemanager.Databasemanager().lengh()}")

        databasemanager.Databasemanager().onserverssave(self.data)
