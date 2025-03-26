import streamlit as st
from datetime import datetime
from ai.travel_assistant import TravelAssistant
from ai.travel_summary import TravelSummary
from api.api_client import TravelAPIClient
from ai.research_assistant import ResearchAssistant
from ai.user_preferences import get_travel_details
from constants import *


def format_date(date_str):
    """Format date string for display and API calls"""
    if isinstance(date_str, datetime):
        return date_str.strftime("%B %d, %Y")
    return date_str

ResearchAssistant._initialize_vector_store()

def initialize_session_state():
    """Initialize all session state variables"""
    if 'search_requirements' not in st.session_state:
        st.session_state.search_requirements = ""

        if 'travel_assistant' not in st.session_state:
        st.session_state.travel_assistant = None
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'research_assistant' not in st.session_state:
        st.session_state.research_assistant = None
    if 'research_messages' not in st.session_state:
        st.session_state.research_messages = []
    if 'parsed_data' not in st.session_state:
        st.session_state.parsed_data = None
    if 'progress_bar' not in st.session_state:
        st.session_state.progress_bar = None


def display_parsed_travel_details(parsed_data):
    """Display and validate parsed travel details"""
    with st.expander("Parsed Travel Details", expanded=True):
        st.markdown("### Here's what we understood:")
        details = {
            "From": parsed_data['origin_airport_code'] or "Not specified",
            "To": parsed_data['destination_airport_code'] or "Not specified",

            "Departure": format_date(parsed_data['start_date']) if parsed_data['start_date'] else "Not specified",
            "Return": format_date(parsed_data['end_date']) if parsed_data['end_date'] else "Not specified",
        }
        
        for key, value in details.items():
            st.write(f"**{key}:** {value}")

            # Validate required fields
        if not (parsed_data['origin_airport_code'] and parsed_data['destination_airport_code']):
            st.error(MISSING_AIRPORTS_ERROR)
            st.stop()
            
        if not (parsed_data['start_date'] and parsed_data['end_date']):
            st.error(MISSING_DATES_ERROR)
            st.stop()

def search_travel_options(parsed_data, travel_description, progress_container):
    """Search for flights and hotels based on parsed data"""
    with progress_container.status("✨ Finding the best options for you...",state="running", expanded=True):
        my_bar = st.progress(0)
        try:
            st.write(" - ✈️ Finding available flights for your dates..")
            flight_response = api_client.search_flights(
                parsed_data['origin_airport_code'],
                parsed_data['destination_airport_code'],
                parsed_data['start_date'],
                parsed_data['end_date'],
                travel_description
            )

            my_bar.progress(0.2)
            if flight_response.status_code != 200:
                st.error(SEARCH_FAILED)
                return False
                
            # Get flight results first
            st.write(" - ✈️ Analyzing flight options and prices...")


            flight_task_id = flight_response.json().get("task_id")
            flight_results = api_client.poll_task_status(flight_task_id, "flight", st)
            if not flight_results:
                st.error(SEARCH_INCOMPLETE)
                return False
            
            my_bar.progress(0.4)
            st.write(" - 🏨 Searching for hotels in your destination...")
            
            hotel_response = api_client.search_hotels(
                parsed_data['destination_city_name'],
                parsed_data['start_date'],
                parsed_data['end_date'],
                1,
                "USD"
            )

            my_bar.progress(0.6)
            if hotel_response.status_code != 200:
                st.error(SEARCH_FAILED)
                return False
                
            # Get hotel results
            st.write(" - 🏨 Finding the best room options for you...")
            
            hotel_task_id = hotel_response.json().get("task_id")
            hotel_results = api_client.poll_task_status(hotel_task_id, "hotel", st)