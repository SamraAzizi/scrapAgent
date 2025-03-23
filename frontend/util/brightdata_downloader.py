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

    def filter_dataset(self, dataset_id: str, filter_params: Dict, records_limit: Optional[int] = None) -> Dict:
        """Initialize dataset filtering and get snapshot ID"""
        url = f"{self.base_url}/datasets/filter"
        payload = {
            "dataset_id": dataset_id,
            "filter": filter_params
        }
        if records_limit:
            payload["records_limit"] = records_limit

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error initiating filter request: {e}")
            raise

    def get_snapshot_status(self, snapshot_id: str) -> Dict:
        """Check the status of a specific snapshot"""
        url = f"{self.base_url}/datasets/snapshots/{snapshot_id}"
        try:
            response = requests.request("GET", url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error checking snapshot status: {e}")
            raise