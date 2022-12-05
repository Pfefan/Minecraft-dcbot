"""Checks for online servers"""
import concurrent.futures

import commands.checkserver_status as checkserver_status
import databasemanager


class Lookup():
    """class to automaticly ping all servers in the database"""
    def __init__(self) -> None:
        self.data = []

    async def serverlookup(self, interaction):
        """Goes through server entries in database and check if the respond,
         if so it will save there data into a database"""
        ipdata = databasemanager.Databasemanager().default_getall()
        lookup = checkserver_status.Statuscheck()

        with concurrent.futures.ThreadPoolExecutor(max_workers=250) as executor:
            # Submit the data to be processed in multiple threads
            results = [executor.submit(lookup.getstatus, ipdata) for ipdata in ipdata]

            # Iterate over the results and get the processed data
            for future in concurrent.futures.as_completed(results):
                if future.result() is not False:
                    self.data.append(future.result())
        print(self.data)

        print(f"found {len(self.data)} servers with players online " +
                f"out of {databasemanager.Databasemanager().default_lengh()}")
        """await ctx.send(f"found {len(self.data)} servers with players " +
                f"online out of {databasemanager.Databasemanager().default_lengh()}")"""

        databasemanager.Databasemanager().on_savedata(self.data) 
        self.data.clear()
