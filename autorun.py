"""Module imports"""
import time
import playeraktivitylookup
import onlineserverlookup

class Autorun():
    """class to run in another thread in the background to watch servers and to check
     what servers are online"""
    def __init__(self) -> None:
        pass

    def main(self):
        """main class"""
        while True:
            for i in range(6):
                playeraktivitylookup.Main().main()
                time.sleep(100)
            onlineserverlookup.Lookup().onlinecmd()
