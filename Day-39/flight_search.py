import os
import requests
from dotenv import load_dotenv

# ---------------------------- LOAD ENVIRONMENT VARIABLES ------------------------------- #

# Load variables from .env file
load_dotenv()

# SerpAPI endpoint
SERPAPI_ENDPOINT = "https://serpapi.com/search"


class FlightSearch:
    """Handles flight searches using the SerpAPI Google Flights API."""

    def __init__(self):
        """Initialize the API key."""

        # Read the API key from environment variables
        self._api_key = os.environ["SERPAPI_API_KEY"]

    def check_flights(
        self,
        origin_city_code,
        destination_city_code,
        from_time,
        to_time,
        is_direct=True,
    ):
        """Search for flights between two airports."""

        # Query parameters for the Google Flights API
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

        
        if is_direct:
            query["stops"] = "1"

        # Send request to SerpAPI
        response = requests.get(
            url=SERPAPI_ENDPOINT,
            params=query
        )

        # Store the search type
        self.is_direct = is_direct

        # Handle unsuccessful HTTP responses
        if response.status_code != 200:
            print(
                f"check_flights() "
                f"response code: "
                f"{response.status_code}"
            )
            return None

        # Convert response into JSON format
        data = response.json()

        # Handle API-specific errors
        if "error" in data:
            print(f"API error: {data['error']}")
            return None

        return data