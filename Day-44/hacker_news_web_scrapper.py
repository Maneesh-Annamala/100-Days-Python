"""
Scrapes Hacker News and displays the article
with the highest number of upvotes.
"""

from bs4 import BeautifulSoup
import requests

# ---------------------------- FETCH WEB PAGE ------------------------------- #

# Send a request to Hacker News
response = requests.get("https://news.ycombinator.com/news")

# Get HTML source code
web_data = response.text

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(web_data, "html.parser")

# ---------------------------- EXTRACT DATA ------------------------------- #

# Get all news articles
headings = soup.select(".athing.submission")

# Get all article scores
points = soup.select(".score")

# ---------------------------- FIND HIGHEST UPVOTED ARTICLE ------------------------------- #

highest_point = float("-inf")
top_news = None

# Compare every article with its score
for heading, point in zip(headings, points):

    # Example: "152 points" → ["152", "points"]
    get_points = point.getText().split()

    # Convert score into integer
    int_point = int(get_points[0])

    # Check if current article has the highest score
    if int_point > highest_point:
        highest_point = int_point
        top_news = heading.getText()

# Display the highest voted article
print(
    f"The highest point news is "
    f"{top_news} with {highest_point} points"
)