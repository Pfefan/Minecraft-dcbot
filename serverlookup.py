"""Module import"""
from mcstatus import JavaServer

class Ping():
    """ping minecraft server"""

    def __init__(self, _threads, _hostname, cmd) -> None:
        self.threads = _threads
        self.hostname = _hostname
        self.tcount = cmd

    def main(self):
        """pings servers and checks if there are any players on the server"""
        counter = 0
        while counter < self.threads:
            try:
                server = JavaServer.lookup(self.hostname[counter] +
                                                ":25565")
                status = server.status()
                self.tcount.data.append((self.hostname[counter], status.version.name,
                                         status.players.online))
            except IOError:
                pass       
            counter += 1

        self.tcount.threadcounter -= 1
