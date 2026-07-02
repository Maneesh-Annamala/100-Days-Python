class FlightData:
    """Represents the details of a flight."""

    def __init__(
        self,
        price,
        origin_airport,
        destination_airport,
        out_date,
        return_date,
    ):
        """Initialize a FlightData object."""

        # Flight price
        self.price = price

        # Departure airport code
        self.origin_airport = origin_airport

        # Arrival airport code
        self.destination_airport = destination_airport

        # Outbound flight date
        self.out_date = out_date

        # Return flight date
        self.return_date = return_date


def find_cheapest_flight(data, return_date):
    """Return the cheapest available flight."""

    # Handle empty or invalid flight data
    if (
        data is None
        or (
            not data.get("best_flights")
            and not data.get("other_flights")
        )
    ):
        print("No flight data")

        return FlightData(
            "N/A",
            "N/A",
            "N/A",
            "N/A",
            "N/A",
        )

    # Combine all available flights into one list
    all_flights = (
        data.get("best_flights", [])
        + data.get("other_flights", [])
    )

    # Use the first flight as the initial cheapest flight
    first_flight = all_flights[0]

    lowest_price = first_flight["price"]

    origin = (
        first_flight["flights"][0]
        ["departure_airport"]["id"]
    )

    destination = (
        first_flight["flights"][-1]
        ["arrival_airport"]["id"]
    )

    out_date = (
        first_flight["flights"][0]
        ["departure_airport"]["time"]
        .split(" ")[0]
    )

    # Store the initial cheapest flight
    cheapest_flight = FlightData(
        lowest_price,
        origin,
        destination,
        out_date,
        return_date,
    )

    # Compare all flights
    for flight in all_flights:

        try:
            price = flight["price"]

        except KeyError:
            print("--- No price available for flight. ---")
            continue

        if price < lowest_price:

            lowest_price = price

            origin = (
                flight["flights"][0]
                ["departure_airport"]["id"]
            )

            destination = (
                flight["flights"][-1]
                ["arrival_airport"]["id"]
            )

            out_date = (
                flight["flights"][0]
                ["departure_airport"]["time"]
                .split(" ")[0]
            )

            cheapest_flight = FlightData(
                lowest_price,
                origin,
                destination,
                out_date,
                return_date,
            )

            print(
                f"Lowest price to "
                f"{destination} is "
                f"GBP {lowest_price}"
            )

    return cheapest_flight