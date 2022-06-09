import asyncio
import onlineserverlookup
import time

class Autorun():
    def __init__(self) -> None:
        pass

    async def main(self):
        online = onlineserverlookup.lookup()
        #await asyncio.gather(online.onlinecmd())
        time.sleep(600)