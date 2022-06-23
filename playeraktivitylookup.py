"""module imports"""
from mcstatus import JavaServer

import editdatabase
import datetime

def main():
    """pings servers an gets amount of players online"""
    dbmanger = editdatabase.Databasemanager()
    servers = dbmanger.plyhistoryall()
    delold()
    for i in servers:
        try:
            status = JavaServer.lookup(i).status()
            dbmanger.plyhistoryinfosave(i, status.players.online)
        except IOError:
            try:
                if len(i.split(":")) == 2:
                    return
                status = JavaServer.lookup(i).status()
                dbmanger.plyhistoryinfosave(i, status.players.online)
            except IOError:
                return

def delold():
    """delete data wich is more than 7 days old"""
    dbmanger = editdatabase.Databasemanager()
    timestamp = dbmanger.plyhistorygettime()
    now = datetime.datetime.now()
    for time in timestamp:
        elapsed = now - time[1]
        if elapsed > datetime.timedelta(days=7):
            dbmanger.plyhistoryautodel(time[0])
