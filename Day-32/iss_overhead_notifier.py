import requests
from datetime import datetime
import smtplib
import time

# Your current latitude and longitude
MY_LAT = 51.507351
MY_LONG = -0.127758

# Email credentials
MY_MAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"


def over_night():
    """Check whether the ISS is currently above your location."""

    # Get the current ISS location
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Check if ISS is within ±5 degrees of your location
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True

    return False


def is_night():
    """Check whether it is currently night at your location."""

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    # Get sunrise and sunset times
    response = requests.get(
        "https://api.sunrise-sunset.org/json",
        params=parameters
    )
    response.raise_for_status()

    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Get current hour
    time_now = datetime.now().hour

    # Return True if it's night
    if time_now >= sunset or time_now <= sunrise:
        return True

    return False


# Keep checking every 60 seconds
while True:

    time.sleep(60)

    # Send email only if ISS is nearby and it's night
    if over_night() and is_night():

        with smtplib.SMTP("smtp.gmail.com") as connection:

            # Secure connection
            connection.starttls()

            # Login to Gmail
            connection.login(MY_MAIL, MY_PASSWORD)

            # Send notification email
            connection.sendmail(
                from_addr=MY_MAIL,
                to_addrs="YOUR RECEIVER EMAIL",
                msg="Subject:ISS NOTIFICATION\n\nThe ISS is above your location and it's currently night. Go outside and try to spot it!"
            )