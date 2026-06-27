import requests

# Parameters sent to the Open Trivia Database API
parameters = {
    "amount": 10,
    "category": 21,
    "difficulty": "medium",
    "type": "boolean",
}

# Send request to fetch quiz questions
response = requests.get(
    "https://opentdb.com/api.php",
    params=parameters
)

# Raise an exception if the request fails
response.raise_for_status()

# Convert API response into JSON format
data = response.json()

# Store only the list of quiz questions
question_data = data["results"]