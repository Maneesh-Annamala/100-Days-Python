"""
Scrapes Empire's Top 100 Movies list and
stores the movie titles in a text file.
"""

import requests
from bs4 import BeautifulSoup

# ---------------------------- FETCH WEB PAGE ------------------------------- #

# Archived Empire Top 100 Movies webpage
URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Send request to the webpage
response = requests.get(url=URL)

# Get HTML source code
web_data = response.text

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(web_data, "html.parser")

# ---------------------------- EXTRACT MOVIE TITLES ------------------------------- #



# Find all movie title headings
titles = soup.find_all(
    name="h3",
    class_="title"
)

# Store every movie title in a list
movie_titles = [title.getText() for title in titles]

# ---------------------------- SAVE MOVIES TO FILE ------------------------------- #

with open("top_movies.txt","a",encoding="utf-8") as file:
    # Reverse the list so that ranking starts from 1
    for movie in movie_titles[::-1]:

        # Replace ')' with '.'
        corrected = movie.replace(")", ".")

        # Write each movie on a new line
        file.write(f"{corrected}\n")