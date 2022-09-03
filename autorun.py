"""Module imports"""
import time
import playeraktivitylookup

class Autorun():
    """class to run in another thread in the background to watch servers and to check
     what servers are online"""
    def __init__(self) -> None:
        self.repeattime = 600

    def main(self):
        """main class"""
        print("started autolookup")
        while True:
            playeraktivitylookup.main()
            time.sleep(self.repeattime)

    async def changerepeattime(self, ctx, _repeattime):
        """function to change repeat time of autolookup"""
        if _repeattime != None and isinstance(int(_repeattime), int) == True:
            self.repeattime = int(_repeattime) * 60
            await ctx.channel.send(f"autolookup intervall successfully changed to {self.repeattime / 60} minutes")
        else:
            await ctx.channel.send("invalid option")
        print(f"changed repeattime to {self.repeattime} seconds")
