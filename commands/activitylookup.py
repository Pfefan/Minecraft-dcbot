"""module imports"""
import datetime

from mcstatus import JavaServer

import databasemanager


def main():
    """pings servers an gets amount of players online"""
    dbmanger = databasemanager.Databasemanager()
    servers = dbmanger.watch_getall()
    delold()
    for i in servers:
        try:
            status = JavaServer.lookup(i).status()
            dbmanger.watch_savedataitem(i, status.players.online)
        except IOError:
            try:
                if len(i.split(":")) == 2:
                    return
                status = JavaServer.lookup(i).status()
                dbmanger.watch_savedataitem(i, status.players.online)
            except IOError:
                return

def delold():
    """delete data wich is more than 7 days old"""
    dbmanger = databasemanager.Databasemanager()
    timestamp = dbmanger.watch_gettimestamps()
    now = datetime.datetime.now()
    for time in timestamp:
        elapsed = now - time[1]
        if elapsed > datetime.timedelta(days=7):
            dbmanger.watch_autodel(time[0])
