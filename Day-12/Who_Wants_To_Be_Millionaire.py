import data

money = 0

# Welcome message
print("Welcome to the KBC!")
print(data.logo)

# Loop through all questions
for i in range(len(data.questions)):

    # Show question and prize money
    print(f"\nYour {data.order[i]} question for ₹{data.price[i]} is:")
    print(data.questions[i])
    print(data.options[i])

    # Get user answer
    user_answer = input("Choose your answer (a/b/c/d): ").lower()

    # Validate input
    while user_answer not in ["a", "b", "c", "d"]:
        user_answer = input("Please choose only a, b, c or d: ").lower()

    # Check answer
    if user_answer == data.answers[i]:
        print(f"Correct answer! You won ₹{data.price[i]}")

        # Update current winnings
        money = data.price[i]

        # Ask if user wants to quit
        quit_game = input("Do you want to quit with current money? (y/n): ").lower()

        while quit_game not in ["y", "n"]:
            quit_game = input("Please choose only y or n: ").lower()

        if quit_game == "y":
            print(f"Your total winnings are ₹{money}")
            break

    else:
        print("Sorry! That's the wrong answer.")

        # Guaranteed winnings check
        if i >= 4:
            print(f"You only got: ₹{money}")
        else:
            print("You won't get any money")

        break