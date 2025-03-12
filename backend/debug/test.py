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

    if not all([origin_airport_code, destination_airport_code, start_date, end_date]):
        return

    url = get_flight_url(
        origin_airport_code, destination_airport_code, start_date, end_date
    )

    # Create API instance
    api = BrightDataAPI()

    # Run flight scraping and hotel search sequentially
    with requests.Session() as session:
        flights = scrape_flights(url, travel_requirements)
        hotels = api.search_hotels(
            session=session,
            occupancy="2",
            currency="USD",
            check_in=start_date,
            check_out=end_date,
            location=destination_city_name,
        )

    response = model.invoke(
        f"""Summarize the following flight and hotels and give me a nicely formatted output: 
        Hotels: {hotels} ||| Flights: {flights}. 
        
        Then make a reccomendation for the best hotel and flight based on this: {travel_requirements}
        
        Note: the price of the flight is maximum of the two prices listed, NOT the combined price.
        """
    )
    print(response.content)


if __name__ == "__main__":
    main()