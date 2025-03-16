from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from ai.context import generate_travel_context_memory
from dotenv import load_dotenv
from ai.models import model
import json
import os
import chromadb

load_dotenv()


class ResearchAssistant:
    embeddings = OllamaEmbeddings(
            model="nomic-embed-text"
        )
    vector_store = None
    
    @staticmethod
    def _clean_metadata_value(value):
        """Clean metadata values to ensure they are valid types"""
        if value is None:
            return ""
        if isinstance(value, (str, int, float, bool)):
            return value
        return str(value)
    
    def __init__(self, context):
        # Initialize the language model
        self.context = context
        self.llm = model
        
        # Initialize the search tool
        search = DuckDuckGoSearchRun()
        
        # Define tools
        self.tools = [
            Tool(
                name="Search",
                func=search.run,
                description="Useful for searching information about travel destinations, attractions, local customs, and travel tips"
            ),
            Tool(
                name="Restaurant_Info",
                func=self.query_restaurant_data,
                description="Use this to get information about restaurants in Thailand including location, ratings, opening hours, and services"
            )
        ]
        
