import time
import playeraktivitylookup

class Autorun():
    def __init__(self) -> None:
        pass

    def main(self):
        while(True):
            playeraktivitylookup.Main().main()
            time.sleep(600)