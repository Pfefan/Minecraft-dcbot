"""module imports"""
from mcstatus import JavaServer

import editdatabase

def main():
    """pings servers an gets amount of players online"""
    dbmanger = editdatabase.Databasemanager()
    servers = dbmanger.plyhistoryall()
    for i in servers:
        try:
            status = JavaServer.lookup(i).status()
            dbmanger.plyhistoryinfosave(i, status.players.online)
        except IOError:
            dbmanger.plyhistoryinfosave(i, "0")
