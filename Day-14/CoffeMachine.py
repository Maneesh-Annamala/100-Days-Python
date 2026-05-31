from machine_data import MENU, resources

money = 0

# Check if enough ingredients are available
def resource_check(order_ingredients):
    """Check whether enough ingredients are available in the machine."""

    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            print(f"Sorry there is not enough {item} in the machine")
            return False

    return True


# Collect money from user
def coins(coffee_type,cost):
    """Calculate total inserted money based on note count."""

    print(f"you selected {coffee_type} and it costs {cost}")

    ten = int(input("Enter how many tens: ")) * 10
    twenty = int(input("Enter how many twenty: ")) * 20
    fifty = int(input("Enter how many fifty: ")) * 50
    hundred = int(input("Enter how many hundred: ")) * 100

    return ten + twenty + fifty + hundred


# Check payment and return change
def enough_money(customer_money, actual_cost):
    """Check whether user inserted enough money."""

    if customer_money >= actual_cost:
        global money

        money += actual_cost
        change = round(customer_money - actual_cost, 2)

        print(f"Here is your change {change} sir!")

        return True

    else:
        print("Sorry! Your money not sufficient, money refunded")
        return False


# Deduct used resources
def deduction(order_ingredients):
    """Deduct ingredients after successful order."""

    for item in order_ingredients:
        resources[item] -= order_ingredients[item]

    print(f"Here is your {customer_req} ☕ enjoy!")
    print("Have a good day.")


coffee = True

while coffee:

    # Ask user for drink selection
    customer_req = input("What would you like? (espresso/latte/cappuccino): ").lower()

    # Turn off machine
    if customer_req == "off":
        coffee = False

    # Show machine report
    elif customer_req == "report":
        print(f"Water : {resources['water']}ml")
        print(f"Milk : {resources['milk']}ml")
        print(f"Coffee : {resources['coffee']}g")
        print(f"Money : {money}")

    # Show total profit
    elif customer_req == "profit":
        print(f"Today total profit is {money}")

    # Process drink order
    elif customer_req in MENU:

        drinks = MENU[customer_req]

        # Check ingredients
        if resource_check(drinks["ingredients"]):

            # Take money
            amount = coins(customer_req,drinks["cost"])

            # Complete purchase if enough money
            if enough_money(amount, drinks["cost"]):
                deduction(drinks["ingredients"])

    # Handle invalid input
    else:
        print(f"Sorry we don't have {customer_req}")