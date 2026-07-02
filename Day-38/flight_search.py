import os
import requests
from dotenv import load_dotenv

# ---------------------------- LOAD ENVIRONMENT VARIABLES ------------------------------- #

# Load variables from .env file
load_dotenv()

# SerpAPI endpoint
SERPAPI_ENDPOINT = "https://serpapi.com/search"


class FlightSearch:
    """Handles flight search requests using the SerpAPI Google Flights API."""

    def __init__(self):
        """Initialize the API key."""

        # Read API key from environment variables
        self._api_key = os.environ["SERPAPI_API_KEY"]

    def check_flights(
        self,
        origin_city_code,
        destination_city_code,
        from_time,
        to_time,
    ):
        """Search for available flights between two airports."""

        # Query parameters for Google Flights
        query = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime("%Y-%m-%d"),
            "return_date": to_time.strftime("%Y-%m-%d"),
            "type": "1",
            "adults": "1",
            "currency": "GBP",
            "api_key": self._api_key,
        }

        # Send request to SerpAPI
        response = requests.get(
            url=SERPAPI_ENDPOINT,
            params=query
        )

        # Raise exception if request fails
        response.raise_for_status()

        # Convert response into JSON
        data = response.json()

        # Check if API returned an error
        if "error" in data:
            print(f"API Error: {data['error']}")
            return None

        return data