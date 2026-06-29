import requests
import smtplib
from email.message import EmailMessage

# ---------------------------- CONSTANTS ------------------------------- #

# Stock information
STOCK = "TSLA"
COMPANY_NAME = "Tesla"

# API Keys
MY_STOCK_API = "YOUR STOCK API KEY"
MY_NEWS_API = "YOUR NEWS API KEY"

# API Endpoints
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Email credentials
MY_MAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"


# ---------------------------- STOCK DATA ------------------------------- #

# Parameters for Alpha Vantage API
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": MY_STOCK_API
}

# Fetch stock data
response = requests.get(
    STOCK_ENDPOINT,
    params=parameters
)

# Raise exception if request fails
response.raise_for_status()

# Convert response into JSON
data = response.json()

# Extract daily stock data
daily_data = data["Time Series (Daily)"]

# Convert dates into a list
daily_data_list = list(daily_data.keys())

# Yesterday's closing price
yesterday_data = float(
    daily_data[daily_data_list[0]]["4. close"]
)

# Day before yesterday's closing price
day_before_yesterday = float(
    daily_data[daily_data_list[1]]["4. close"]
)

# Calculate percentage change
difference = abs(yesterday_data - day_before_yesterday)
percentage_change = (
    difference / day_before_yesterday
) * 100


# ---------------------------- NEWS FETCHING ------------------------------- #

# Fetch news only if stock changed significantly
if percentage_change > 5:

    news_parameters = {
        "q": COMPANY_NAME,
        "from": daily_data_list[0],
        "sortBy": "publishedAt",
        "apikey": MY_NEWS_API
    }

    # Fetch latest news
    news_response = requests.get(
        NEWS_ENDPOINT,
        params=news_parameters
    )

    news_response.raise_for_status()

    news_data = news_response.json()

    # Get all articles
    all_articles = news_data["articles"]

    # Select top 3 articles
    three_articles = all_articles[:3]

    # Connect to Gmail SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:

        # Secure the connection
        connection.starttls()

        # Login to Gmail
        connection.login(
            MY_MAIL,
            MY_PASSWORD
        )

        # Send each article as a separate email
        for article in three_articles:

            msg = EmailMessage()

            msg["Subject"] = article["title"]
            msg["From"] = MY_MAIL
            msg["To"] = "YOUR RECEIVER EMAIL"

            # Email body
            msg.set_content(article["description"])

            connection.send_message(msg)

    print("News emails sent successfully!")

else:
    print("Stock change is less than 1%. No email sent.")