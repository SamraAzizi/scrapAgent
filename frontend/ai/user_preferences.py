from dotenv import load_dotenv
from ai.models import model

load_dotenv()

class TravelSummary:
    def __init__(self):
        self.model = model