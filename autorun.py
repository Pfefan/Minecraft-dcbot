"""Module imports"""
import time
import playeraktivitylookup

class Autorun():
    """class to run in another thread in the background to watch servers and to check
     what servers are online"""
    def __init__(self) -> None:
        pass

    def main(self):
        """main class"""
        while True:
            playeraktivitylookup.main()
            time.sleep(600)
