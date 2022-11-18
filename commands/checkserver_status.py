"""Module import"""
from mcstatus import JavaServer

class Lookup():
    """ping minecraft server"""

    def __init__(self, _threads, _hostname, lk_self) -> None:
        self.threads = _threads
        self.hostname = _hostname
        self.lookup_self = lk_self

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
                self.lookup_self.data.append((self.hostname[counter], status.version.name,
                                        status.players.online))
            except IOError:
                pass
            counter += 1

        self.lookup_self.threadcounter -= 1
