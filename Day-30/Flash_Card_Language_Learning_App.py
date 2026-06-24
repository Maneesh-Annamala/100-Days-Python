from tkinter import *
import pandas
import random

# Background color used throughout the application
BACKGROUND_COLOR = "#B1DDC6"

# Stores the currently displayed card
current_card = {}

# Stores the words that still need to be learned
to_learn = {}

# Try loading saved progress
try:
    data = pandas.read_csv("data/words_to_learn.csv")

# If progress file doesn't exist, load original French words
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    print(original_data)

    # Convert dataframe into list of dictionaries
    to_learn = original_data.to_dict(orient="records")

# Load saved progress
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    """Display a new random French word card."""

    global current_card, flip_timer

    # Cancel previous timer before starting a new one
    window.after_cancel(flip_timer)

    # Select a random word
    current_card = random.choice(to_learn)

    # Show French side of card
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")

    # Display front card image
    canvas.itemconfig(card_background, image=card_front_img)

    # Flip card after 3 seconds
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    """Flip the flashcard and display the English translation."""

    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")

    # Display back card image
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    """Remove known word from learning list and save progress."""

    # Remove current word from remaining words
    to_learn.remove(current_card)

    print(len(to_learn))

    # Save remaining words
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

    # Show next card
    next_card()


# ---------------------------- UI SETUP ------------------------------- #

# Main application window
window = Tk()

window.title("Flashy")

window.config(
    padx=50,
    pady=50,
    bg=BACKGROUND_COLOR
)

# Initial flip timer
flip_timer = window.after(3000, func=flip_card)

# Flashcard canvas
canvas = Canvas(width=800, height=526)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

# Card background image
card_background = canvas.create_image(
    400,
    263,
    image=card_front_img
)

# Language title
card_title = canvas.create_text(
    400,
    150,
    text="",
    font=("Ariel", 40, "italic")
)

# Word text
card_word = canvas.create_text(
    400,
    263,
    text="",
    font=("Ariel", 60, "bold")
)

canvas.config(
    bg=BACKGROUND_COLOR,
    highlightthickness=0
)

canvas.grid(
    row=0,
    column=0,
    columnspan=2
)

# Wrong answer button
cross_image = PhotoImage(file="images/wrong.png")

unknown_button = Button(
    image=cross_image,
    highlightthickness=0,
    command=next_card
)

unknown_button.grid(row=1, column=0)

# Correct answer button
check_image = PhotoImage(file="images/right.png")

known_button = Button(
    image=check_image,
    highlightthickness=0,
    command=is_known
)

known_button.grid(row=1, column=1)

# Display first card
next_card()

window.mainloop()