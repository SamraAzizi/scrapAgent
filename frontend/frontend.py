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
