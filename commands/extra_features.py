"""Some features which is used multiple times"""
import time
from threading import Thread

import requests
from prettytable import PrettyTable as pt


class Features():
    """functions to execute in the discord bot"""

    def __init__(self) -> None:
        """class variables"""
        self.players = ""
        self.threadcounter = 0


    def getplayernames(self, server):
        """Looping through user query server (12 players) as long it doesnt have all playernames"""
        status = server.status()
        self.threadcounter = 0
        online = status.players.online

        if online == 0 and status.players.sample is None:
            return "no players online"
        elif online > 0 and status.players.sample is None:
            return "No responce"

        self.players = [item.name for item in status.players.sample]


        if len(self.players) == 0:
            return"responce list is empty"

        if online > 12:
            if len(self.players) == 1:
                return f"server modified responce: {self.players[0]}"
            while len(self.players) < online:
                status = server.status()
                Thread(target=self.playersearch(status)).start()
                while self.threadcounter > 200:
                    time.sleep(0.1)
        return self.players

    def playersearch(self, status):
        """Loops through all players currently online in the server"""
        self.threadcounter += 1
        for i in status.players.sample:
            if i.name not in self.players:
                self.players.append(i.name)
        self.threadcounter -= 1


    def geolocation(self, ipaddress):
        """gets the geolocation of the server"""

        request_url = 'http://ip-api.com/json/' + ipaddress
        response = requests.get(request_url).json()

        if response['status'] == 'fail' and len(ipaddress.split(":")) > 1:
            request_url = 'http://ip-api.com/json/' + ipaddress.split(":")[0]
            response = requests.get(request_url).json()

        georesult = response

        if str(georesult['status']) == "success":
            flag = ":flag_" +  georesult["countryCode"].lower() + ":"
            return f"Country: {georesult['country']} {flag} | state: {georesult['regionName']}" + \
                f"| city: {georesult['city']} | IPv4: {georesult['query']} \n" + \
                f"ISP: {georesult['isp']} | timezone: {georesult['timezone']}"
        elif str(georesult['status']) == "fail":
            return f"failed to get geolocation of {self.georesult['query']}"

    def tablegen(headers, data):
        """func to generate tables"""
        """func to generate tables"""

        tb = pt()

        tb.field_names = headers
        tb.add_rows(data)
        
        return tb
