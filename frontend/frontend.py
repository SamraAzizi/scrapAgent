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