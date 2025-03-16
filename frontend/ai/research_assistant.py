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
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.memory.chat_memory.add_ai_message(
            generate_travel_context_memory(self.context)
        )
        
        # Initialize the agent
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True
        )
        
        # Set initial system message
        self.system_message = """You are a travel research assistant specializing in Thailand. 
        Help users learn about local restaurants, attractions, travel tips, and other travel-related information. 
        Use the Restaurant_Info tool to find specific details about restaurants in Thailand, and the search tool 
        for general travel information. Always be helpful and informative."""
    
    @classmethod  
    def _initialize_vector_store(cls):
        """Initialize and populate the vector store with restaurant data"""
        print("Starting vector store initialization...")
        
        # Configure Chroma settings
        client_settings = chromadb.Settings(
            anonymized_telemetry=False,
            is_persistent=True
        )
        
        # Check if vector store already exists
        if os.path.exists("restaurant_db"):
            print("Found existing restaurant_db, loading...")
            cls.vector_store = Chroma(
                persist_directory="restaurant_db",
                embedding_function=cls.embeddings,
                client_settings=client_settings
            )
            return cls.vector_store
        
        # Load restaurant data
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, '..', 'data', 'thailand_restaurants.json')
            print(f"Loading restaurant data from: {data_path}")
            
            with open(data_path, 'r', encoding='utf-8') as f:
                restaurants_data = json.load(f)
                total = len(restaurants_data)
                print(f"Successfully loaded {total} restaurants")
        except FileNotFoundError as e:
            print(f"Error: Could not find restaurant data file: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in restaurant data: {e}")
            return None
        
        # Prepare documents for vector store
        documents = []
        metadatas = []
        
        for i, restaurant in enumerate(restaurants_data):
            # Show progress every 10%
            if i % (total // 10) == 0:
                print(f"Processing restaurants: {(i/total)*100:.1f}% complete...")
            
            # Format opening hours
            open_hours = ""
            if restaurant.get('open_hours'):
                for day, hours in restaurant['open_hours'].items():
                    open_hours += f"{day}: {hours}\n"
            
            # Create a detailed text description for each restaurant
            text = f"""
            Name: {restaurant.get('name', 'N/A')}
            Category: {restaurant.get('category', 'N/A')}
            Address: {restaurant.get('address', 'N/A')}
            Rating: {restaurant.get('rating', 'N/A')} ({restaurant.get('reviews_count', 0)} reviews)
            Opening Hours:
            {open_hours}
            Current Status: {restaurant.get('open_hours_updated', 'N/A')}
            Phone: {restaurant.get('phone_number', 'N/A')}
            Website: {restaurant.get('open_website', 'N/A')}
            Price Range: {restaurant.get('price_range', 'N/A')}
            Services: {str(restaurant.get('services_provided', 'N/A'))}
            Location: Lat {restaurant.get('lat', 'N/A')}, Lon {restaurant.get('lon', 'N/A')}
            """
            
            documents.append(text)
            metadatas.append({
                "name": cls._clean_metadata_value(restaurant.get('name')),
                "category": cls._clean_metadata_value(restaurant.get('category')),
                "rating": cls._clean_metadata_value(restaurant.get('rating', 0)),
                "reviews_count": cls._clean_metadata_value(restaurant.get('reviews_count', 0)),
                "price_range": cls._clean_metadata_value(restaurant.get('price_range'))
            })
        
        # Create and persist vector store
  