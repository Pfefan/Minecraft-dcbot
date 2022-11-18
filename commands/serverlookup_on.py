"""Checks for online servers"""
import time
from threading import Thread

import commands.checkserver_status as checkserver_status
import databasemanager

class Lookup():
    """class to automaticly ping all servers in the database"""
    def __init__(self) -> None:
        self.data = []
        self.threadcounter = 0

    async def serverlookup(self):
        """Goes through server entries in database and check if the respond,
         if so it will save there data into a database"""
        self.data.clear()
        threadlengh = 10
        adresses = databasemanager.Databasemanager().default_getall()
        outadresses = []
        ping_threads = []

        for adress in adresses:
            while self.threadcounter > 200:
                time.sleep(0.1)
            outadresses.append(adress)
            if len(outadresses) >= threadlengh:
                lookup = checkserver_status.Lookup(threadlengh, outadresses.copy(),
                                           self)
                pingthread = Thread(target=lookup.main)
                ping_threads.append(pingthread)
                pingthread.start()
                self.threadcounter += 1
                outadresses.clear()

        for pingthread in ping_threads:
            pingthread.join()

        print(f"found {len(self.data)} servers with players online " +
                f"out of {databasemanager.Databasemanager().default_lengh()}")

        databasemanager.Databasemanager().on_savedata(self.data)
