import requests
from flights.google_flight_scraper import get_flight_url, scrape_flights
from user_preferences import get_travel_details
from backend.flights.hotels import BrightDataAPI
from config.models import model


def main():
    travel_requirements = input("Enter your travel requirements: ")
    details = get_travel_details(travel_requirements)

    origin_airport_code = details.get("origin_airport_code")
    destination_airport_code = details.get("destination_airport_code")
    destination_city_name = details.get("destination_city_name")
    if not details.get("dates"):
        return
    start_date, end_date = details["dates"].get("start_date"), details["dates"].get(
        "end_date"
    )
