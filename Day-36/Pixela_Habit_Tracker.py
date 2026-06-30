import requests
from datetime import datetime

# ---------------------------- CONSTANTS ------------------------------- #

# Base Pixela API URL
PIXELA_URL = "https://pixe.la/v1/users"

# Pixela account details
TOKEN = "YOUR TOKEN"
USERNAME = "YOUR USERNAME"
GRAPH_ID = "graph1"

# ---------------------------- CREATE USER ------------------------------- #

# User registration details
details = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# Create a new Pixela user (Run only once)
# response = requests.post(
#     url=PIXELA_URL,
#     json=details
# )
# print(response.text)

# ---------------------------- CREATE GRAPH ------------------------------- #

# Graph endpoint
GRAPH_URL = f"{PIXELA_URL}/{USERNAME}/graphs"

# Authentication header
headers = {
    "X-USER-TOKEN": TOKEN,
}

# Graph configuration
graphs_data = {
    "id": GRAPH_ID,
    "name": "Coding Graph",
    "unit": "hours",
    "type": "float",
    "color": "momiji",
}

# Create graph (Run only once)
# graph_response = requests.post(
#     url=GRAPH_URL,
#     json=graphs_data,
#     headers=headers
# )
# print(graph_response.text)

# ---------------------------- ADD PIXEL ------------------------------- #

# Get today's date
today = datetime.now()

# Pixel creation endpoint
PIXELA_URL_FOR_POST = f"{GRAPH_URL}/{GRAPH_ID}"

# Ask user for today's study hours
quantity = input("Enter how many hours you studied today: ")

# Today's study record
post_details = {
    "date": today.strftime("%Y%m%d"),
    "quantity": quantity,
}

# Add today's pixel
post_response = requests.post(
    url=PIXELA_URL_FOR_POST,
    json=post_details,
    headers=headers
)

print(post_response.text)

# ---------------------------- DELETE PIXEL ------------------------------- #

# Endpoint to delete today's record
delete_url = (
    f"{PIXELA_URL_FOR_POST}/"
    f"{today.strftime('%Y%m%d')}"
)

# Delete today's record (Run when needed)
# delete_response = requests.delete(
#     url=delete_url,
#     headers=headers
# )
# print(delete_response.text)

# ---------------------------- UPDATE PIXEL ------------------------------- #

# Endpoint to update today's record
update_url = (
    f"{PIXELA_URL_FOR_POST}/"
    f"{today.strftime('%Y%m%d')}"
)

# Updated study hours
update_data = {
    "quantity": "7.5"
}

# Update today's record (Run when needed)
# update_response = requests.put(
#     url=update_url,
#     json=update_data,
#     headers=headers
# )
# print(update_response.text)