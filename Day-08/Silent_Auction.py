# Function to find the highest bidder
def silent_auction(Detailed_information):

    winner = ""
    highest_bid = 0

    # Check each bidder and compare bid amounts
    for j in Detailed_information:

        bid_amount = Detailed_information[j]

        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = j

    # Display the auction winner
    print(f"The winner is {winner} with the highest bid {highest_bid}")


# Control auction flow
Bid_Over = False

# Store bidder details
Details = {}

while not Bid_Over:

    # Get bidder name and bid amount
    Name = input("What is your name?").lower()
    price = int(input("Your bid price?"))

    # Save bidder information
    Details[Name] = price

    # Check if more bidders are remaining
    others = input("if others are there type 'YES' otherwise type 'NO'").lower()

    # End auction and show winner
    if others == "no":
        Bid_Over = True
        silent_auction(Details)

    # Clear screen for next bidder
    else:
        print("\n" * 100)