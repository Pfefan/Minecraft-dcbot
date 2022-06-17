"""module imports"""
from mcstatus import JavaServer

import editdatabase


class Main:
    """Manage playeraktivies on servers"""
    def __init__(self):
        self.dbmanger = editdatabase.Databasemanager()

    def main(self):
        """pings servers an gets amount of players online"""
        servers = self.dbmanger.plyhistoryall()
        for i in servers:
            try:
                status = JavaServer.lookup(i).status()
                self.dbmanger.plyhistoryinfosave(i, status.players.online)
            except IOError:
                self.dbmanger.plyhistoryinfosave(i, "0")
