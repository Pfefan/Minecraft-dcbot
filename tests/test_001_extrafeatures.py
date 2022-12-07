"""Tests for extrafeatures class"""
from unittest.mock import Mock
import pytest

from commands.extra_features import PlayerNameService
from commands.extra_features import GeolocationService


def test_001_getplayernames():
    """Testing getting player name method"""
    # Create a mock server object
    server = Mock()
    feature_class = PlayerNameService()

    # Test the case where there are no players online
    server.status.return_value.players.online = 0
    server.status.return_value.players.sample = None
    result = feature_class.getplayernames(server, test=True)  # Set test=True to specify test environment
    assert result == "no players online"

    # Test the case where there are some players online, but no response from the server
    server.status.return_value.players.online = 5
    server.status.return_value.players.sample = None
    result = feature_class.getplayernames(server, test=True)  # Set test=True to specify test environment
    assert result == "No responce"

    # Test the case where there are some players online, and the server returns a response
    server.status.return_value.players.online = 5
    server.status.return_value.players.sample = [{"name": "player1"}, {"name": "player2"}, {"name": "player3"}, {"name": "player4"}, {"name": "player5"}]
    result = feature_class.getplayernames(server, test=True)  # Set test=True to specify test environment
    assert result == ["player1", "player2", "player3", "player4", "player5"]

    # Test the case where there are more than 12 players online, and the server returns a response with only one player name
    server.status.return_value.players.online = 15
    server.status.return_value.players.sample = [{"name": "player1"}]
    result = feature_class.getplayernames(server, test=True)  # Set test=True to specify test environment
    assert result == "server modified responce: player1"

    # Test the case where there are more than 12 players online, and the server returns a response with multiple player names
    server.status.return_value.players.online = 13
    server.status.return_value.players.sample = [{"name": "player1"}, {"name": "player2"}, {"name": "player3"}, {"name": "player4"}, {"name": "player5"}, {"name": "player6"}, {"name": "player7"}, {"name": "player8"}, {"name": "player9"}, {"name": "player10"}, {"name": "player11"}, {"name": "player12"}, {"name": "player13"}]
    result = feature_class.getplayernames(server, test=True)
    assert result == ["player1", "player2", "player3", "player4", "player5", "player6", "player7", "player8", "player9", "player10", "player11" ,"player12" ,"player13"]  # Verify that the returned list contains all 15 player names

def test_geolocation():
    """Test geolocation"""
    # Get the geolocation of an IP address
    service = GeolocationService()
    ip_address = "8.8.8.8"
    geolocation = service.geolocation(ip_address)

    # Assert that the response contains the expected data
    assert geolocation["country"] == "United States"
    assert geolocation["flag"] == ":flag_us:"
    assert geolocation["state"] == "Virginia"
    assert geolocation["city"] == "Ashburn"
    assert geolocation["ipv4"] == ip_address
    assert geolocation["isp"] == "Google LLC"
    assert geolocation["timezone"] == "America/New_York"

    ip_address = "invalid"
    geolocation = service.geolocation(ip_address)

    # Assert that the response contains the expected error message
    assert geolocation["error"] == f"failed to get geolocation of {ip_address}"
