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

# Load variables from .env file
load_dotenv()

MY_MAIL = os.getenv("MY_MAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

# ---------------------------- REQUEST CACHE ------------------------------- #

# Cache API responses to reduce unnecessary API requests
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

# Fetch all subscribed customer email addresses
customer_emails = data_manager.get_customer_emails()

# ---------------------------- DATE SETTINGS ------------------------------- #

# Search flights from tomorrow
tomorrow = datetime.now() + timedelta(days=1)

# Search flights up to six months from today
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# Departure airport (London Heathrow)
ORIGIN_CITY_IATA = "LHR"

# ---------------------------- EMAIL NOTIFICATION ------------------------------- #

def notification_sender(data):
    """Send flight deal notifications to all subscribed customers."""

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:

        # Secure the SMTP connection
        connection.starttls()

        # Login to Gmail
        connection.login(
            MY_MAIL,
            MY_PASSWORD
        )

        # Send the notification to every customer
        for mail in customer_emails:

            msg = EmailMessage()

            msg["Subject"] = "Low price alert!"
            msg["From"] = MY_MAIL
            msg["To"] = mail

            # Email body
            msg.set_content(data)

            connection.send_message(msg)


# ---------------------------- SEARCH FLIGHTS ------------------------------- #

for destination in sheet_data:

    pprint(
        f"Getting flights for "
        f"{destination['city']}..."
    )

    # Search direct flights
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

    print(
        f"{destination['city']}: "
        f"GBP {cheapest_flight.price}"
    )

    # If no direct flights are available,
    # search again including stopover flights
    if cheapest_flight.price == "N/A":

        print(
            f"No direct flight for "
            f"{destination['city']}. "
            f"Searching indirect flights..."
        )

        stopover_flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False
        )

        cheapest_flight = find_cheapest_flight(
            stopover_flights,
            return_date=six_month_from_today.strftime("%Y-%m-%d")
        )

        print(
            f"{destination['city']}: "
            f"GBP {cheapest_flight.price}"
        )

    # Check whether a cheaper flight was found
    if (
        cheapest_flight.price != "N/A"
        and cheapest_flight.price < destination["lowestPrice"]
    ):

        pprint(
            f"Lower price flight found "
            f"to {destination['city']}!"
        )

        # Update the lowest price in Google Sheets
        data_manager.update_lowest_price(
            destination["id"],
            cheapest_flight.price
        )

        # Create a different email if the flight has stopovers
        if cheapest_flight.stops > 0:

            data = (
                f"Low price alert! Only GBP "
                f"{cheapest_flight.price} to fly\n\n"
                f"We found the best deal through "
                f"indirect/multiple flights.\n\n"
                f"From: {cheapest_flight.origin_airport}\n"
                f"To: {cheapest_flight.destination_airport}\n"
                f"Departure: {cheapest_flight.out_date}\n"
                f"Return: {cheapest_flight.return_date}"
            )

            notification_sender(data)

        else:

            data = (
                f"Low price alert! Only GBP "
                f"{cheapest_flight.price} to fly\n\n"
                f"From: {cheapest_flight.origin_airport}\n"
                f"To: {cheapest_flight.destination_airport}\n"
                f"Departure: {cheapest_flight.out_date}\n"
                f"Return: {cheapest_flight.return_date}"
            )

            notification_sender(data)