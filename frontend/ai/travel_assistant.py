from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
from ai.models import model
from ai.context import generate_travel_context_memory

load_dotenv()


