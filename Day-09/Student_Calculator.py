# Calculator functions
def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def division(n1, n2):
    return n1 / n2

# Store operators and functions
operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": division,
}

# Run calculator
calculation = True

while calculation:

    # Get first number
    first_number = float(input("Enter first number: "))

    # Show available operations
    for i in operations:
        print(i)

    # Get operator and second number
    operator = input("Choose what you want to perform: ")
    second_number = float(input("Enter second mumber: "))

    # Calculate result
    Total = operations[operator](first_number, second_number)
    print(f"Your Total Value: {Total}")

    again = True

    # Continue calculation with previous result
    while again:

        repeat = input("Type 'Y' if you want to continue with {Total} or 'N' for fresh start").lower()

        if repeat == "y":

            # Show operations again
            for i in operations:
                print(i)

            # Get next operation and number
            operator = input("Choose what you want to perform: ")
            second_number = float(input("Enter second mumber: "))

            # Update total
            Total = operations[operator](Total, second_number)
            print(f"Your Total Value: {Total}")

        # Start fresh
        elif repeat == "n":
            again = False
            print("\n" * 40)