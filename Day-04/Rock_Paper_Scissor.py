import random

# Welcome message
print("welcome to the rock paper scissors game")

# Get user's move
your_move = int(input("what do you choose? Type 0 for rock, 1 for paper, 2 for scissors:"))

# Show the user's choice
if your_move == 0:
    print("you chose rock")
elif your_move == 1:
    print("you chose paper")
elif your_move == 2:
    print("you chose scissors")
else:
    print("you chose not a valid move")

# Generate computer move
computer_choose = ["rock", "paper", "scissors"]
computer_move = random.randint(0, 2)

# Show computer's choice
if computer_move == 0:
    print("computer chose rock")
elif computer_move == 1:
    print("computer chose paper")
else:
    print("computer chose scissors")

# Compare moves and decide the winner
if your_move == computer_move:
    print("its a draw")
elif your_move == 0 and computer_move == 1:
    print("computer won!")
elif your_move == 1 and computer_move == 0:
    print("you won!")
elif your_move == 2 and computer_move == 1:
    print("you won!")
elif your_move == 1 and computer_move == 2:
    print("computer won!")
elif your_move == 0 and computer_move == 2:
    print("you won!")
else:
    print("computer won")