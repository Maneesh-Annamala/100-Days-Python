# Initial seat data
seats = {
    1: "ravi",
    2: None,
    3: "teja",
    4: None,
    5: "ram",
    6: None,
    7: None,
    8: "sai",
    9: None,
    10: None
}

# Store passengers when all seats are full
waiting_list = []

print("Welcome to the seat booking platform")

checking = True

while checking:

    try:
        # Show menu
        chose = int(input("1.Available seats\n2.Book ticket\n3.Cancel ticket\n4.Passenger list\n5.Exit\nPlease select: "))

    except ValueError:
        print("You need to choose between those options")
        continue

    # Show available seats
    if chose == 1:

        for key, value in seats.items():
            if value is None:
                print(f"{key} is available")

    # Book ticket
    elif chose == 2:

        name = input("Enter your name: ").lower()

        # Check whether at least one seat is available
        is_available = False

        for key, value in seats.items():
            if value is None:
                is_available = True
                break

        if is_available:

            try:
                seat_number = int(input(f"Enter what seat you want from 1 - {len(seats)}: "))

            except ValueError:
                print("You need to enter numbers only!")
                continue

            # Validate seat number
            if seat_number not in seats:
                print(f"We don't have that seat number! Choose between 1-{len(seats)}")
                continue

            # Ask again if seat is already booked
            while seats[seat_number] is not None:

                print("That seat already booked! Please choose another one")

                try:
                    seat_number = int(input("Enter what seat you want: "))

                except ValueError:
                    print("You need to enter numbers only")

                if seat_number not in seats:
                    print("That number is not available")

                else:
                    continue

            # Confirm booking
            if seats[seat_number] is None:
                seats[seat_number] = name
                print("Your ticket reservation was successful!")

        else:
            # Add passenger to waiting list
            if name not in waiting_list:
                waiting_list.append(name)
                print("You are added to waiting list")

            else:
                print("You are already in waiting list!")

    # Cancel ticket
    elif chose == 3:

        passenger_name = input("Enter your name: ").lower()

        try:
            reservation_num = int(input("Enter your reservation number: "))

        except ValueError:
            print("You need to enter seat number in numbers!")
            continue

        # Validate seat number
        if reservation_num not in seats:
            print("We don't have that seat number!")
            continue

        # Make sure seat is booked
        while seats[reservation_num] is None:

            print("That seat is not booked! Please enter your seat number")

            try:
                reservation_num = int(input("Enter your reservation number: "))

            except ValueError:
                print("You need to enter numbers only")

            if reservation_num not in seats:
                print("That number is not available")

            else:
                continue

        # Verify passenger details
        if passenger_name != seats[reservation_num]:
            print("That seat is on some other passenger's name")
            continue

        # Cancel reservation
        seats[reservation_num] = None
        print("Your ticket was cancelled successfully!")

        # Assign seat to first waiting passenger
        if waiting_list:
            seats[reservation_num] = waiting_list[0]
            waiting_list.pop(0)

    # Show passenger list
    elif chose == 4:

        print("Passengers list:")

        found = False

        for key, value in seats.items():
            if value is not None:
                print(value)
                found = True

        if not found:
            print("There are no passengers!")

    # Exit program
    elif chose == 5:
        checking = False