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

    def _poll_results(
        self, session: requests.Session, response_id: str, max_retries: int = 10, delay: int = 10
    ) -> Optional[Dict]:
        """Generic polling function for any type of search results."""
        for _ in range(max_retries):
            try:
                response = session.get(
                    f"{self.BASE_URL}/get_result",
                    params={
                        "customer": self.CUSTOMER_ID,
                        "zone": self.ZONE,
                        "response_id": response_id,
                    },
                    headers=self.headers,
                )
                if response.status_code == 200:
                    try:
                        result = response.json()
                        return result
                    except ValueError as e:
                        print(f"Failed to parse JSON response: {e}")
                        print("Raw response:", response.text[:200])

                time.sleep(delay)

            except Exception as e:
                print(f"Error polling results: {e}")

        return None


