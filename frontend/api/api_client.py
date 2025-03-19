import requests
import time

class TravelAPIClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def search_flights(self, origin, destination, start_date, end_date, preferences):
        """Send flight search request"""
        response = requests.post(
            f"{self.base_url}/search_flights",
            json={
                "origin": origin,
                "destination": destination,
                "start_date": start_date,
                "end_date": end_date,
                "preferences": preferences
            }
        )
        return response
    
     def search_hotels(self, location, check_in, check_out, occupancy, currency):
        """Send hotel search request"""
        response = requests.post(
            f"{self.base_url}/search_hotels",
            json={
                "location": location,
                "check_in": check_in,
                "check_out": check_out,
                "occupancy": occupancy,
                "currency": currency
            }
        )
        return response