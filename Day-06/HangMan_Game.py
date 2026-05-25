import random
from hangman_words import word_list
import hangman_art

# Set total lives for the player
lives = 6

# Display game logo
print(hangman_art.logo)

# Pick a random word from the word list
chosen_word = random.choice(word_list)
print(chosen_word)

# Create placeholders based on word length
placeholder = ""
word_length = len(chosen_word)

for position in range(word_length):
    placeholder += "_"

print("Word to guess: " + placeholder)

# Track game state and correct guesses
game_over = False
correct_letters = []

# Main game loop
while not game_over:

    # Show remaining lives
    print(f"**{lives}/6 LIVES LEFT***")

    # Ask player to guess a letter
    guess = input("Guess a letter: ").lower()

    display = ""

    # Check if letter was already guessed
    if guess in correct_letters:
        print(f"you already guessed {guess}")

    # Update word display
    for letter in chosen_word:

        if letter == guess:
            display += letter
            correct_letters.append(guess)

        elif letter in correct_letters:
            display += letter

        else:
            display += "_"

    print("Word to guess: " + display)

    # Reduce life for wrong guess
    if guess not in chosen_word:
        lives -= 1
        print(f"you guessed {guess}, that's not in word.you loose a life ")

        # End game if no lives left
        if lives == 0:
            game_over = True
            print(f"**IT WAS {chosen_word}!YOU LOSE**")

    # Check if player guessed the word
    if "_" not in display:
        game_over = True
        print("**YOU WIN**")

    # Show hangman stage based on remaining lives
    print(hangman_art.stages[lives])