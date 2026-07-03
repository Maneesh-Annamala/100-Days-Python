import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# ---------------------------- LOAD ENVIRONMENT VARIABLES ------------------------------- #

# Load variables from .env file
load_dotenv()

# Sheety endpoints
SHEETY_PRICES_ENDPOINT = (
    "https://api.sheety.co/a69f34703ef46a646822a31cf6e31049/"
    "flightDealChecker/prices"
)

SHEETY_USERS_ENDPOINT = (
    "https://api.sheety.co/a69f34703ef46a646822a31cf6e31049/"
    "flightDealChecker/users"
)


class DataManager:
    """Handles all communication with the Sheety API."""

    def __init__(self):
        """Initialize authentication and destination data."""

        # Read Sheety credentials from environment variables
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]

        # Create authentication object
        self._authorization = HTTPBasicAuth(
            self._user,
            self._password
        )

        # Stores destination data from Google Sheets
        self.destination_data = {}

    def get_destination_data(self):
        """Fetch all destination details from Google Sheets."""

        # Send GET request to retrieve flight destinations
        response = requests.get(
            url=SHEETY_PRICES_ENDPOINT,
            auth=self._authorization
        )

        # Raise an exception if the request fails
        response.raise_for_status()

        # Convert response into JSON format
        data = response.json()

        # Store destination data
        self.destination_data = data["prices"]

        return self.destination_data

    # ---------------------------- UPDATE LOWEST PRICE ------------------------------- #

    def update_lowest_price(self, row_id, new_price):
        """Update the lowest flight price for a destination."""

        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }

        # Send PUT request to update the spreadsheet
        response = requests.put(
            url=f"{SHEETY_PRICES_ENDPOINT}/{row_id}",
            json=new_data,
            auth=self._authorization
        )

        # Raise an exception if the update fails
        response.raise_for_status()

    # ---------------------------- GET CUSTOMER EMAILS ------------------------------- #

    def get_customer_emails(self):
        """Fetch all registered customer email addresses."""

        # Send GET request to retrieve user data
        users_response = requests.get(
            url=SHEETY_USERS_ENDPOINT,
            auth=self._authorization
        )

        # Raise an exception if the request fails
        users_response.raise_for_status()

        # Convert response into JSON format
        user_data = users_response.json()

        # Store all customer email addresses
        user_emails = []

        for email in user_data["users"]:

            mail = email["enterYourEmail"]

            user_emails.append(mail)

        return user_emails