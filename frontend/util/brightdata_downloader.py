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