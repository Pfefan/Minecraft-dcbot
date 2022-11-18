"""Module imports"""
import time
import commands.activitylookup as activitylookup

class Autorun():
    """class to run in another thread in the background to watch servers and to check
     what servers are online"""
    def __init__(self) -> None:
        self.repeattime = 600

    def main(self):
        """main class"""
        print("started autolookup")
        while True:
            activitylookup.main()
            time.sleep(self.repeattime)

    async def changerepeattime(self, ctx, _repeattime):
        """function to change repeat time of autolookup"""
        if _repeattime is not None and isinstance(int(_repeattime), int) is True:
            self.repeattime = int(_repeattime) * 60
            await ctx.response.send_message(f"autolookup intervall successfully changed to {self.repeattime / 60} minutes")
        else:
            await ctx.response.send_message("invalid option")
        print(f"changed repeattime to {self.repeattime} seconds")
