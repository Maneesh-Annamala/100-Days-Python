# Display a welcome message and explain the mission to the player
print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.")

# Ask the player to choose a direction at the crossroads
choice1 = input("you are at cross roads to find the treasure take left or right:")

# Check if the player chooses the correct path
if choice1 == "left":

    # Ask the player whether to swim or wait
    choice2 = input("swim or wait :")

    # Continue the game only if the player chooses to wait
    if choice2 == "wait":

        # Ask the player to choose a door color
        choice3 = input("red , yellow and blue :")

        # Check the selected door and display the result
        if choice3 == "red":
            print("you loose")

        elif choice3 == "yellow":
            print("you win")

        elif choice3 == "blue":
            print("you loose!")

        # Handle invalid input or unexpected choices
        else:
            print("you choose smthng soo you loose")

    # End the game if the player chooses to swim
    else:
        print("game over")

# End the game if the player chooses the wrong direction
else:
    print("game over")