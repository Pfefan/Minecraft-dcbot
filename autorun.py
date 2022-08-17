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
        print("started autolookup")
        while True:
            try:
                playeraktivitylookup.main()
            except Exception as e:
                print(e)
            time.sleep(600)
