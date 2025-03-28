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
