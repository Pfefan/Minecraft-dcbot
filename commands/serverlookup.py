"""Module import"""
from mcstatus import JavaServer

class Lookup():
    """ping minecraft server"""

    def __init__(self, _threads, _hostname, cmd) -> None:
        self.threads = _threads
        self.hostname = _hostname
        self.tcount = cmd

    def main(self):
        """pings servers and checks if there are any players on the server"""
        counter = 0
        port = "25565"
        while counter < self.threads:
            if len(self.hostname[counter].split(":")) < 2:
                port = ":25565"
            else:
                port = ""
            try:
                server = JavaServer.lookup(self.hostname[counter] +
                                                port)
                status = server.status()
                self.tcount.data.append((self.hostname[counter], status.version.name,
                                        status.players.online))
            except IOError:
                pass
            counter += 1

        self.tcount.threadcounter -= 1
