"""Some features which is used multiple times"""
import asyncio
import time
from threading import Thread

import requests


class PlayerNameService():
    """functions to execute in the discord bot"""

    def __init__(self) -> None:
        """class variables"""
        self.players = []
        self.threadcounter = 0


    def getplayernames(self, server, test=False):
        """Looping through user query server (12 players) as long it doesnt have all playernames"""
        self.threadcounter = 0
        self.players.clear()
        status = server.status()
        online = status.players.online

        if online == 0 and status.players.sample is None:
            return "no players online"
        elif online > 0 and status.players.sample is None:
            return "No responce"

        # Use the test parameter to determine how to access the player names
        if test:
            self.players = [item["name"] for item in status.players.sample]
            # Use item["name"] for test environment
        else:
            self.players = [item.name for item in status.players.sample]
            # Use item.name for normal runtime

        if len(self.players) == 0:
            return"responce list is empty"

        if online > 12:
            if len(self.players) == 1:
                return f"server modified responce: {self.players[0]}"
            while len(self.players) < online:
                status = server.status()
                Thread(target=self.playersamples(status)).start()
                while self.threadcounter > 200:
                    time.sleep(0.1)
        return self.players


    def playersamples(self, status):
        """Loops through all players currently online in the server"""
        self.threadcounter += 1
        for i in status.players.sample:
            if i.name not in self.players:
                self.players.append(i.name)
        self.threadcounter -= 1


class GeolocationService:
    """Class to handel user interactions with geolocation"""
    def __init__(self):
        self.api_url = "http://ip-api.com/json/"

    def geolocation(self, ipaddress):
        """gets the geolocation of the server"""

        # Make the API request
        response = self._get_response(ipaddress)

        # Check the status of the response
        if str(response['status']) == "success":
            # Format the geolocation data as a dictionary
            data = {
                "country": response["country"],
                "flag": ":flag_" +  response["countryCode"].lower() + ":",
                "state": response["regionName"],
                "city": response["city"],
                "ipv4": response["query"],
                "isp": response["isp"],
                "timezone": response["timezone"],
            }
            return data
        else:
            return {
                "error": f"failed to get geolocation of {ipaddress}"
            }

    def _get_response(self, ipaddress):
        """Makes the API request"""
        request_url = self.api_url + ipaddress
        try:
            # Use the `requests` module to make the API request
            response = requests.get(request_url, timeout=10)
            # Parse the response as JSON
            return response.json()
        except TimeoutError:
            # Return an error if the request fails
            return {
                "status": "failed",
                "message": f"Failed to get response from {request_url}"
            }
