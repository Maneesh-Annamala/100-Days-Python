import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# ---------------------------- LOAD ENVIRONMENT VARIABLES ------------------------------- #

# Load variables from .env file
load_dotenv()

# Sheety endpoint
SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/your_endpoint/prices"


class DataManager:
    """Handles all communication with the Sheety API."""

    def __init__(self):
        """Initialize authentication and destination data."""

        # Read Sheety credentials
        self._user = os.getenv("SHEETY_USERNAME")
        self._password = os.getenv("SHEETY_PASSWORD")

        # Create HTTP Basic Authentication object
        self._authorization = HTTPBasicAuth(
            self._user,
            self._password
        )

        # Stores destination data from Google Sheets
        self.destination_data = {}

    def get_destination_data(self):
        """Fetch destination data from Google Sheets."""

        # Send GET request to Sheety
        response = requests.get(
            url=SHEETY_PRICES_ENDPOINT,
            auth=self._authorization
        )

        # Raise exception if request fails
        response.raise_for_status()

        # Convert response into JSON
        data = response.json()

        # Store destination data
        self.destination_data = data["prices"]

        return self.destination_data

    # ---------------------------- UPDATE LOWEST PRICE ------------------------------- #

    def update_lowest_price(self, row_id, new_price):
        """Update the lowest flight price in Google Sheets."""

        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }

        # Send PUT request to update spreadsheet
        response = requests.put(
            url=f"{SHEETY_PRICES_ENDPOINT}/{row_id}",
            json=new_data,
            auth=self._authorization
        )

        # Raise exception if update fails
        response.raise_for_status()