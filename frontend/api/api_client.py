import requests
import time

class TravelAPIClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url