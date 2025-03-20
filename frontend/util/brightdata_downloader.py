import requests
import time
from typing import Dict, Optional
from dotenv import load_dotenv
import os

load_dotenv()

class BrightDataDownloader:
    def __init__(self):
        self.base_url = "https://api.brightdata.com"
        self.auth_token = os.getenv('BRIGHTDATA_API_KEY')
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }