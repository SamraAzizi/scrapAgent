import os
import requests
import time
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from datetime import datetime

load_dotenv()


class BrightDataAPI:
    BASE_URL = "https://api.brightdata.com/serp"
    CUSTOMER_ID = "c_8a10678a"
    ZONE = "serp_api1"

    def __init__(self):
        self.api_key = os.getenv("BRIGHTDATA_API_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }



