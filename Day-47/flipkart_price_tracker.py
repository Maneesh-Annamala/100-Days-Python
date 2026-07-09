"""
Tracks the price of a Flipkart product and
sends an email notification when the price
drops below the target price.
"""

import requests
import os
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv

# ---------------------------- LOAD ENVIRONMENT VARIABLES ------------------------------- #

# Load variables from .env file
load_dotenv()

# Target price for notification
MY_PRICE = 85000

# Email credentials
MY_MAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

# ---------------------------- REQUEST HEADERS ------------------------------- #

# Browser headers to avoid request blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9",
    "Referer": "https://www.google.com/",
}

# Flipkart product URL
URL = (
    "https://www.flipkart.com/apple-iphone-17-sage-256-gb/p/itmcfa57eff7729c?"
    "pid=MOBHFN6YNAG4ZTHS&lid=LSTMOBHFN6YNAG4ZTHSWUQQUI&"
    "marketplace=FLIPKART&q=iphone&store=tyy%2F4io&"
    "srno=s_1_1&otracker=search&otracker1=search&"
    "fm=organic&iid=2204d24f-c0fa-4707-988e-f11002f86be6."
    "MOBHFN6YNAG4ZTHS.SEARCH&ppt=None&ppn=None&"
    "ssid=fdztus3n400000001783637554189&"
    "qH=0b3f45b266a97d70&ov_redirect=true"
)

# ---------------------------- FETCH PRODUCT PAGE ------------------------------- #

# Send request to Flipkart
response = requests.get(
    URL,
    headers=headers
)

# Raise exception if request fails
response.raise_for_status()

# Parse HTML
web_data = response.text
soup = BeautifulSoup(
    web_data,
    "html.parser"
)

# ---------------------------- EXTRACT PRODUCT DETAILS ------------------------------- #

# Get product price
price_tag = soup.select_one(
    ".v1zwn21l.v1zwn20._1psv1zeb9._1psv1ze0"
)

# Stop execution if price element is missing
if price_tag is None:
    raise Exception(
        "Price element not found. "
        "Flipkart HTML may have changed."
    )

# Remove ₹ symbol and commas
price = price_tag.getText()[1:].split(",")

# Convert price into integer
final_price = int("".join(price))

# Get product name
product_check = soup.select_one(
    ".v1zwn21l.v1zwn26._1psv1zeb9._1psv1ze0")
if product_check is None:
    raise Exception(
        "product name element not found. "
        "Flipkart HTML may have changed."
    )

product_name = product_check.getText()



# ---------------------------- SEND EMAIL ALERT ------------------------------- #

# Send an email if the product price is below the target price
if final_price < MY_PRICE:

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as connection:

        # Secure the SMTP connection
        connection.starttls()

        # Login to Gmail
        connection.login(
            MY_MAIL,
            MY_PASSWORD
        )

        # Send email notification
        connection.sendmail(
            from_addr=MY_MAIL,
            to_addrs=MY_MAIL,
            msg=(
                f"Subject:Price Drop Alert\n\n"
                f"{product_name}\n\n"
                f"Current Price: ₹{final_price}"
            )
        )

    print("Message sent successfully")