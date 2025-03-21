"""Constants for the frontend application."""

# Search Tab
TRAVEL_DESCRIPTION_HELP = "Tell us about your trip including where you're flying from/to, dates, number of travelers, and any preferences."
TRAVEL_DESCRIPTION_PLACEHOLDER = """Example: I want to fly from LAX to NYC from December 1st, 2024 to December 8th, 2024. 
2 travelers, prefer morning flights, need hotel with wifi and gym. 
Budget around $1000 for flight and $200/night for hotel in USD."""

# Loading States
LOADING_STATES = {
    "flights": {
        "message": "✈️ Searching Flights",
        "description": """Checking airlines • Finding routes • Comparing prices"""
    },
    "hotels": {
        "message": "🏨 Finding Hotels",
        "description": """Searching rooms • Checking amenities • Comparing rates"""
    },
    "processing": {
        "message": "✨ Creating Your Trip",
        "description": """Analyzing options • Optimizing choices • Preparing summary"""
    }
}