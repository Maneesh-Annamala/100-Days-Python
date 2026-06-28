import requests
import smtplib

# ---------------------------- CONSTANTS ------------------------------- #

# Your location
MY_LATITUDE = 17.3850
MY_LONGITUDE = 78.4867

# OpenWeather API Key
OWN_API = "YOUR API KEY"

# Email credentials
MY_MAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"

# API request parameters
parameters = {
    "lat": MY_LATITUDE,
    "lon": MY_LONGITUDE,
    "appid": OWN_API,
    "cnt": 4
}

# ---------------------------- WEATHER CHECK ------------------------------- #

# Request weather forecast data
response = requests.get(
    "https://api.openweathermap.org/data/2.5/forecast",
    params=parameters
)

# Raise exception if request fails
response.raise_for_status()

# Convert response into JSON format
data = response.json()

# Flag to check if rain is expected
will_rain = False

# Check weather conditions for the next few forecasts
for weather in data["list"]:

    condition = weather["weather"][0]["id"]

    # Weather IDs below 700 indicate rain, snow, drizzle, etc.
    if condition < 700:
        will_rain = True

# ---------------------------- SEND EMAIL ------------------------------- #

# Send notification if rain is expected
if will_rain:

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:

        # Secure connection
        connection.starttls()

        # Login to Gmail
        connection.login(MY_MAIL, MY_PASSWORD)

        # Send weather alert email
        connection.sendmail(
            from_addr=MY_MAIL,
            to_addrs="YOUR RECEIVER EMAIL",
            msg="Subject:Weather Update\n\n"
                "☔ It's going to rain today.\n"
                "Remember to take your umbrella!"
        )

    print("Message sent successfully!")

else:
    print("No rain expected today.")