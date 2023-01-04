"""Module import"""
from mcstatus import JavaServer
import dns.resolver

class Statuscheck():
    """ping minecraft server"""

    def __init__(self) -> None:
        pass

    def getstatus(self, address):
        """pings servers and checks if there are any players on the server"""
        ipsplit = address.split(":")
        try:
            if len(ipsplit) != 2:
                server = JavaServer.lookup(address + "25565", timeout=2)
            else:
                server = JavaServer.lookup(address, timeout=2)
            status = server.status()
            return ((address, status.version.name, status.players.online))
        except IOError:
            return False
        except dns.resolver.LifetimeTimeout:
            return False
        except dns.resolver.NoNameservers:
            return False
