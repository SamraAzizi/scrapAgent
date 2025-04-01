# AI Travel Companion 🌍✈️

Welcome to the AI Travel Companion, your smart travel assistant that simplifies trip planning by helping you find flights, accommodations, dining options, and local recommendations.

## Features
### 🔎 Intelligent Travel Search
- Understands natural language travel queries
- Automatically extracts dates, locations, and preferences
- Searches flights and hotels in real-time
- Tracks search progress for a better user experience

### 🤖 AI-Assisted Guidance
- **Trip Planner**: Assists with itinerary creation and travel arrangements
- **Local Guide**: Offers insights on destinations, attractions, and eateries
- Advanced restaurant search using vector-based retrieval (currently available for Thailand only)
- Integrates with web search for updated travel information

### 🏨 Detailed Travel Insights
- Flight options with pricing details
- Curated hotel recommendations
- Restaurant suggestions with:
  - Ratings and user reviews
  - Operating hours
  - Address and contact information
  - Estimated price range
  - Available amenities

### 💬 Interactive Chat Support
- Conversational AI for seamless trip planning
- Suggested prompts to guide users
- Context-aware responses tailored to individual travel needs
- Rich-text output for better readability

## Tech Stack
- **Frontend**: Streamlit
- **AI Models**: Ollama/Claude
- **Vector Database**: ChromaDB
- **Text Embeddings**: nomic-embed-text
- **Search Engine**: DuckDuckGo API
- **Data Management**: JSON & Vector Storage
- **Live Web Data (Scraping, APIs, Datasets)**: BrightData

## Getting Started

### Install Required Packages
```bash
pip install -r requirements.txt