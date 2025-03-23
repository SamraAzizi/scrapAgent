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

    def download_snapshot(self, snapshot_id: str, output_file: str) -> None:
        """Download the snapshot data and save to file"""
        time.sleep(5)
        url = f"{self.base_url}/datasets/snapshots/{snapshot_id}/download"
        try:
            response = requests.request("GET", url, headers=self.headers)
            response.raise_for_status()
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Data successfully saved to {output_file}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading snapshot: {e}")
            raise

    def poll_and_download(self, dataset_id: str, filter_params: Dict, 
                         output_file: str, records_limit: Optional[int] = None, 
                         max_retries: int = 30, delay: int = 10) -> None:
        """Complete workflow: Filter dataset, poll for completion, and download results"""
        # Initialize the filter request
        print("Initiating dataset filter request...")
        filter_response = self.filter_dataset(dataset_id, filter_params, records_limit)
        snapshot_id = filter_response.get('snapshot_id')


        if not snapshot_id:
            raise ValueError("No snapshot ID received in response")
        
        print(f"Received snapshot ID: {snapshot_id}")
        
        # Poll for completion