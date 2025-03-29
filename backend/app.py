from flask import Flask, request, jsonify
from flights.google_flight_scraper import get_flight_url, scrape_flights
from flights.hotels import BrightDataAPI
import requests
import asyncio
import uuid
import threading
from enum import Enum
from collections import defaultdict
from waitress import serve


app = Flask(__name__)

# In-memory storage for task results
task_results = defaultdict(dict)
# Lock for thread-safe operations on task_results
task_lock = threading.Lock()

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

def run_async(coro):
    """Helper function to run async code"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

def update_task_status(task_id, status, data=None, error=None):
    """Thread-safe update of task status"""
    with task_lock:
        if data is not None:
            task_results[task_id].update({
                'status': status,
                'data': data
            })
        elif error is not None:
            task_results[task_id].update({
                'status': status,
                'error': error
            })
        else:
            task_results[task_id]['status'] = status

def update_task_status(task_id, status, data=None, error=None):
    """Thread-safe update of task status"""
    with task_lock:
        if data is not None:
            task_results[task_id].update({
                'status': status,
                'data': data
                })
        elif error is not None:
            task_results[task_id].update({
                'status': status,
                'error': error
            })
        else:
            task_results[task_id]['status'] = status


def process_flight_search(task_id, origin, destination, start_date, end_date, preferences):
    try:
        # Update status to processing
        update_task_status(task_id, TaskStatus.PROCESSING.value)