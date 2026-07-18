from flask import Flask
import random

"""
A simple Flask number guessing game.

The user visits the home page, chooses a number
between 0 and 9 in the URL, and the application
responds whether the guess is too high, too low,
or correct with a GIF.
"""

app = Flask(__name__)
# Generate a random number between 0 and 9
num = random.randint(0,9)
# ---------------------------- HOME PAGE ---------------------------- #

@app.route("/")
def display():
    """Displays the welcome page with instructions."""

    return f"<h1>Guess a number between 0 and 9</h1>\
        <img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif' width=400 height=400>"

# ---------------------------- CHECK USER GUESS ---------------------------- #

@app.route("/<int:number>")
def check_number(number):
    """Compares the user's guess with a randomly generated number."""

    # User guessed higher than the generated number
    if number > num:
        return "<h1 style='color:red'>Too high,try again</h1>\
            <img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif' width=200 height=200>"

    # User guessed lower than the generated number
    elif number < num:
        return "<h1 style= 'color:blue'>Too Low,try again</h1>\
            <img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif' width=200 height=200>"

    # User guessed correctly
    elif number == num:
        return "<h1 style= 'color:green'>You Guessed correct</h1>\
            <img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif' width=200 heigth=200>"

# ---------------------------- RUN APPLICATION ---------------------------- #

if __name__ == "__main__":
    app.run(debug=True)