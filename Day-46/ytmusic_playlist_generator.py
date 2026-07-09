"""
Creates a YouTube Music playlist using the
Billboard Hot 100 songs from a selected date.
"""

import os
import requests
import sys
from bs4 import BeautifulSoup
from ytmusicapi import YTMusic

# ---------------------------- YOUTUBE MUSIC LOGIN ------------------------------- #

# Authenticate using browser.json
ytmusic = YTMusic("browser.json")

# Check whether browser.json exists
if not os.path.exists("browser.json"):
    print("The path doesn't exist")
    sys.exit()

# ---------------------------- GET BILLBOARD SONGS ------------------------------- #

URL = "https://appbrewery.github.io/bakeboard-hot-100/"

# Ask the user for a date
user_date = input(
    "Enter your desired date "
    "in this format (YYYY-MM-DD): "
)

# Request Billboard webpage
response = requests.get(f"{URL}{user_date}/")

# Raise exception if request fails
response.raise_for_status()

# Parse HTML
songs_data = response.text
soup = BeautifulSoup(
    songs_data,
    "html.parser"
)

# ---------------------------- EXTRACT SONGS ------------------------------- #

# Get all song titles
songs_titles = soup.find_all(
    name="h3",
    class_="chart-entry__title"
)

# Get all artist names
artist_names = soup.find_all(
    name="span",
    class_="chart-entry__artist"
)

# Store song titles
songs = [
    title.getText()
    for title in songs_titles
]

# Store artist names
artists = [
    artist.getText()
    for artist in artist_names
]

# ---------------------------- CREATE OR FIND PLAYLIST ------------------------------- #

playlists = ytmusic.get_library_playlists()

playlist_name = (
    f"{user_date} top songs"
)

playlist_id = None
found = False

# Check if playlist already exists
for name in playlists:

    if name["title"] == playlist_name:

        found = True

        playlist_id = name["playlistId"]

        print(
            "Playlist with that "
            "name already exists!"
        )

        break

# Create playlist if it doesn't exist
if not found:

    playlist_id = ytmusic.create_playlist(
        title=playlist_name,
        description=(
            f"Playlist containing the "
            f"top songs from {user_date}"
        ),
    )

# ---------------------------- SEARCH SONGS ------------------------------- #

video_ids = []

# Search every song in YouTube Music
for song, singer in zip(
    songs,
    artists,
):

    try:

        song_search = ytmusic.search(
            query=f"{song} {singer}",
            filter="songs",
        )

        if not song_search:

            print(
                f"{song} "
                f"was not found."
            )

            continue

        video_ids.append(
            song_search[0]["videoId"]
        )

        print(
            f"Added: "
            f"{song} by {singer}"
        )

    except Exception:
        continue

# ---------------------------- ADD SONGS TO PLAYLIST ------------------------------- #

add_to_playlist = ytmusic.add_playlist_items(
    playlistId=playlist_id,
    videoIds=video_ids,
)

print(len(video_ids))
print(add_to_playlist)