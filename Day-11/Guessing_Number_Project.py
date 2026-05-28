#Guessing Number Game by Maneesh
import random
from mine import logo

# Generate random number
number = random.randint(1, 100)

# Check player's guess
def level():
    print(f"you have {i} attempts remaining to guess the number")

    guess = int(input("Make a guess: "))

    # Validate number range
    if guess > 100 and guess < 1:
        print("The number is between 1 and 100.so choose between those numbers")
        return False

    # Hint if guess is high
    elif guess > number:
        print("Too high, try again")
        return False

    # Hint if guess is low
    elif guess < number:
        print("Too low, try again")
        return False

    # Player guessed correctly
    else:
        print(f"You guessed the right number {number}.You won!")
        return True

# Show game intro
print(logo)
print("Welcome to the Number Guessing Project")
print("I am thinking of a number between 1 and 100")

game_over = False

while not game_over:

    # Select difficulty level
    difficulty = input("you have 3 levels \n Easy \n Hard \n Extreme. \nType your difficulty: ").lower()

    # Easy mode with 10 attempts
    if difficulty == "easy":
        for i in range(10, 0, -1):
            result = level()

            if result:
                break

            if i == 1:
                print(f"you ran out of guesses!.The nnumber is {number}")

        game_over = True

    # Hard mode with 5 attempts
    elif difficulty == "hard":
        for i in range(5, 0, -1):
            result = level()

            if result:
                break

            if i == 1:
                print(f"you ran out of guesses!.The nnumber is {number}")

        game_over = True

    # Extreme mode with 3 attempts
    elif difficulty == "extreme":
        for i in range(3, 0, -1):
            result = level()

            if result:
                break

            if i == 1:
                print(f"you ran out of guesses!.The nnumber is {number}")

        game_over = True

    # Handle invalid difficulty input
    else:
        print("please choose only between those 3 levels")