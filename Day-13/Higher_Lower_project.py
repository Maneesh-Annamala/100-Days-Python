import random
from art import logo
from art import vs
from game_data import data

# Format account details for display
def formatted_data(account):
    """Format account data for display."""
    account_name = account["name"]
    account_desc = account["description"]
    account_country = account["country"]

    return f"{account_name}, {account_desc}, {account_country}"

score = 0
account_b = random.choice(data)
game_continue = True

while game_continue:
    # Show logo
    print(logo)

    # Assign previous B account as A
    account_a = account_b
    account_b = random.choice(data)

    # Avoid duplicate accounts
    while account_a == account_b:
        account_b = random.choice(data)

    # Show comparison data
    print(f"Compare A: {formatted_data(account_a)}")
    print(vs)
    print(f"Compare B: {formatted_data(account_b)}")

    # Get user guess
    guess = input("Who has more insta followers? Type 'A' or 'B': ").lower()

    while guess not in ["a", "b"]:
        guess = input("Please choose only 'A' or 'B': ").lower()

    print("\n" * 20)
    print(logo)

    # Get follower counts
    account_followers_a = account_a["follower_count"]
    account_followers_b = account_b["follower_count"]

    # Find correct answer
    if account_followers_a > account_followers_b:
        correct_answer = "a"
    else:
        correct_answer = "b"

    # Check user guess
    if guess == correct_answer:
        score += 1
        print(f"You guessed right. Your score is {score}")
    else:
        print(f"You guessed wrong. Your final score is {score}")
        game_continue = False