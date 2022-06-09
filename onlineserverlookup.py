"""Module impots"""
import time
from threading import Thread

import editdatabase
import serverlookup
import time


class lookup():
    """class to automaticly ping all servers in the database"""
    def __init__(self) -> None:
        self.data = []
        self.threadcounter = 0

    async def onlinecmd(self):
        """class to search through the hole database for servers with players online"""
        self.data.clear()
        threadlengh = 10
        adresses = editdatabase.Databasemanager().all()
        outadresses = []
        ping_threads = []

        #infomsg = await ctx.channel.send("searching for servers with" +
        #                                 " players online")

        print("search for servers")

        for adress in adresses:
            while self.threadcounter > 200:
                time.sleep(0.1)
            outadresses.append(adress)
            if len(outadresses) >= threadlengh:
                lookup = serverlookup.Ping(threadlengh, outadresses.copy(),
                                           self)
                pingthread = Thread(target=lookup.main)
                ping_threads.append(pingthread)
                pingthread.start()
                self.threadcounter += 1
                outadresses.clear()

        for pingthread in ping_threads:
            pingthread.join()

        print(f"found {len(self.data)} servers with players online " +
                f"out of {editdatabase.Databasemanager().lengh()}")

        #await infomsg.delete()

        #await ctx.channel.send(f"found {len(self.data)} servers with players online " +
        #        f"out of {editdatabase.Databasemanager().lengh()} use -online to view")
        editdatabase.Databasemanager().onserverssave(self.data)

if "__main__" == __name__:
    lookup().onlinecmd()
    time.sleep(1800)
