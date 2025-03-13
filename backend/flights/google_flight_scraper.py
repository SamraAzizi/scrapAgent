from playwright.async_api import async_playwright
from browser_use import Agent, Browser, BrowserConfig
from config.models import model
from flights.util import flight_scrape_task
from dotenv import load_dotenv
import os

load_dotenv()

class FlightSearchScraper:
    async def start(self, use_bright_data=True):
        self.playwright = await async_playwright().start()

        if use_bright_data:
            # Bright Data configuration
            self.browser = await self.playwright.chromium.connect(
                os.getenv("BRIGHTDATA_WSS_URL")
            )
        else:
            # Local browser configuration
            self.browser = await self.playwright.chromium.launch(
                headless=True,  # Set to True for headless mode
            )

        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

