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
        datalen = len(ipdata)
        lookup = checkserver_status.Statuscheck()

        with concurrent.futures.ThreadPoolExecutor(max_workers=250) as executor:
            # Use the map method to apply the lookup.getstatus function to each element of the ipdata sequence
            results = executor.map(lookup.getstatus, ipdata)

            progresscounter = 0
            # Iterate over the results and get the processed data
            for result in results:
                if result is not False:
                    self.data.append(result)
                    await interaction.edit_original_response(content="Looking for online Servers"+
                                                            f"! {progresscounter} out of "+
                                                            f"{datalen}, {len(self.data)} "+
                                                            "responded")
                progresscounter += 1

        print(f"found {len(self.data)} servers with players online " +
                f"out of {databasemanager.Databasemanager().default_lengh()}")
        await interaction.edit_original_response(content=f"found {len(self.data)} servers with players " +
                f"online out of {datalen}")

        databasemanager.Databasemanager().on_savedata(self.data)
        self.data.clear()
