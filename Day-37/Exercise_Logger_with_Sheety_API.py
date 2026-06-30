import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# ---------------------------- LOAD ENVIRONMENT VARIABLES ------------------------------- #

# Load variables from .env file
load_dotenv()

# API credentials
API_KEY = os.getenv("API_KEY")
API_ID = os.getenv("API_ID")
SHEETY_TOKEN = os.getenv("BEARER_AUTH")

# ---------------------------- CONSTANTS ------------------------------- #

BASE_URL = "https://app.100daysofpython.dev"

POST_URL = f"{BASE_URL}/v1/nutrition/natural/exercise"

SHEETY_URL = (
    "https://api.sheety.co/"
    "a69f34703ef46a646822a31cf6e31049/"
    "workoutTracking/workouts"
)

# Nutritionix API headers
headers = {
    "Content-Type": "application/json",
    "x-app-id": API_ID,
    "x-app-key": API_KEY,
}

# ---------------------------- GET USER INPUT ------------------------------- #

# Ask user about today's workout
exercise = input("Enter what you did today: ")

data = {
    "query": exercise
}

# ---------------------------- FETCH EXERCISE DATA ------------------------------- #

# Send workout description to Nutritionix
response = requests.post(
    url=POST_URL,
    json=data,
    headers=headers
)

# Raise exception if request fails
response.raise_for_status()

# Extract exercise information
post_data = response.json()["exercises"]

# ---------------------------- DATE & TIME ------------------------------- #

today_date = datetime.now().strftime("%Y/%m/%d")
present_time = datetime.now().strftime("%X")

# ---------------------------- SHEETY AUTHORIZATION ------------------------------- #

sheety_headers = {
    "Authorization": SHEETY_TOKEN,
}

# ---------------------------- SAVE WORKOUT DATA ------------------------------- #

# Upload each detected exercise to Google Sheets
for sheet in post_data:

    sheet_input = {
        "workout": {
            "date": today_date,
            "time": present_time,
            "exercise": sheet["name"].title(),
            "duration": sheet["duration_min"],
            "calories": sheet["nf_calories"]
        }
    }

    sheety_response = requests.post(
        url=SHEETY_URL,
        json=sheet_input,
        headers=sheety_headers
    )

    print(sheety_response.text)