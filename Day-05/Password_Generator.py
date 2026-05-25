import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# Welcome message
print("Welcome to the PyPassword Generator!")

# Get password requirements from the user
nr_letters = int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input("How many symbols would you like?\n"))
nr_numbers = int(input("How many numbers would you like?\n"))

# Store password characters in a list
password = []

# Add random letters
for i in range(nr_letters):
    password.append(random.choice(letters))

# Add random symbols
for i in range(nr_symbols):
    password.append(random.choice(symbols))

# Add random numbers
for i in range(nr_numbers):
    password.append(random.choice(numbers))

# Shuffle the password characters
random.shuffle(password)

# Convert list into string
strong_password = "".join(password)

# Print final password
print(strong_password)