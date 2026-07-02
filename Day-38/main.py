import requests_cache
import os
from pprint import pprint
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# ---------------------------- LOAD ENVIRONMENT VARIABLES ------------------------------- #

# Load environment variables from .env
load_dotenv()

MY_MAIL = os.getenv("MY_MAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

# ---------------------------- REQUEST CACHE ------------------------------- #

# Cache API responses to reduce unnecessary requests
requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    }
)

# ---------------------------- SETUP ------------------------------- #

# Create DataManager object
data_manager = DataManager()

# Fetch destination data from Google Sheets
sheet_data = data_manager.get_destination_data()

# Create FlightSearch object
flight_search = FlightSearch()

# ---------------------------- DATE SETTINGS ------------------------------- #

# Search flights starting from tomorrow
tomorrow = datetime.now() + timedelta(days=1)

# Search flights up to six months from today
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# Origin airport (London Heathrow)
ORIGIN_CITY_IATA = "LHR"

# ---------------------------- SEARCH FLIGHTS ------------------------------- #

for destination in sheet_data:

    pprint(f"Getting flights for {destination['city']}...")

    # Search available flights
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    # Find the cheapest flight
    cheapest_flight = find_cheapest_flight(
        flights,
        return_date=six_month_from_today.strftime("%Y-%m-%d")
    )

    pprint(
        f"{destination['city']}: "
        f"GBP {cheapest_flight.price}"
    )

    # Send notification only if a cheaper flight is found
    if (
        cheapest_flight.price != "N/A"
        and cheapest_flight.price < destination["lowestPrice"]
    ):

        pprint(
            f"Lower price flight found "
            f"to {destination['city']}!"
        )

        # Update Google Sheet with the new lowest price
        data_manager.update_lowest_price(
            destination["id"],
            cheapest_flight.price
        )

        # ---------------------------- EMAIL ALERT ------------------------------- #

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as connection:

            # Secure the connection
            connection.starttls()

            # Login to Gmail
            connection.login(
                MY_MAIL,
                MY_PASSWORD
            )

            msg = EmailMessage()

            msg["Subject"] = "Low Price Flight Alert!"
            msg["From"] = MY_MAIL
            msg["To"] = MY_MAIL

            # Email body
            msg.set_content(
                f"Low price alert!\n\n"
                f"Only GBP {cheapest_flight.price}\n\n"
                f"From: {cheapest_flight.origin_airport}\n"
                f"To: {cheapest_flight.destination_airport}\n"
                f"Departure: {cheapest_flight.out_date}\n"
                f"Return: {cheapest_flight.return_date}"
            )

            # Send email
            connection.send_message(msg)