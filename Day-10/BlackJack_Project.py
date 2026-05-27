# Blackjack Project By Maneesh
import random

# Deal a random card
def deal_cards():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    card = random.choice(cards)
    return card

# Calculate total score
def calculate_score(f_cards):
    # Check for blackjack
    if sum(f_cards) == 21 and len(f_cards) == 2:
        return 0

    # Convert Ace value if score exceeds limit
    if 11 in f_cards and sum(f_cards) > 21:
        f_cards.remove(11)
        f_cards.append(1)

    return sum(f_cards)

# Compare final scores and show result
def compare(u_score, c_score):
    if c_score == 0:
        print("You lose!")
    elif u_score == 0:
        print("You won!")
    elif u_score > 21:
        print("Exceeds limit, You Bust!")
        print("You lose!")
    elif c_score > 21:
        print("Exceeds, Computer Bust!")
        print("You won!")
    elif u_score > c_score:
        print("You won!")
    elif c_score > u_score:
        print("You lose!")
    else:
        print("its a draw!")

# Main game logic
def play_game():
    user_cards = []
    computer_cards = []
    user_score = -1
    computer_score = -1

    # Give starting cards
    for _ in range(2):
        user_cards.append(deal_cards())
        computer_cards.append(deal_cards())

    game_over = False

    while not game_over:
        # Update scores
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)

        # Show current cards
        print(f"your cards: {user_cards} , current value:{user_score}")
        print(f"computer first card: {computer_cards[0]}")

        # Stop game if blackjack or bust
        if computer_score == 0 or user_score == 0 or user_score > 21:
            game_over = True
        else:
            # Ask player for another card
            another = input("do you want to draw another card ?(y/n): ").upper()

            while another not in ["Y", "N"]:
                another = input("Choose only between 'Y' or 'N'").upper()

            if another == "Y":
                user_cards.append(deal_cards())
            else:
                game_over = True

    # Computer draws until reaching minimum score
    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_cards())
        computer_score = calculate_score(computer_cards)

    # Show final cards
    print(f"you final hand:{user_cards} , total:{user_score}")
    print(f"computer cards:{computer_cards},total:{computer_score}")

    # Show winner
    compare(user_score, computer_score)

# Run game repeatedly
m_running = True

while m_running:
    initial_step = input("you want to play the blackjack game type 'Y' for yes or 'N' for no: ").lower()

    if initial_step == "y":
        print("\n" * 30)
        play_game()

    elif initial_step == "n":
        m_running = False

    else:
        print("please enter 'Y' or 'N' only!")