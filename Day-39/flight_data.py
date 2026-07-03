class FlightData:
    """Represents the details of a flight."""

    def __init__(
        self,
        price,
        origin_airport,
        destination_airport,
        out_date,
        return_date,
        stops,
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

        # Number of stopovers
        self.stops = stops


def find_cheapest_flight(data, return_date):
    """Find and return the cheapest available flight."""

    # Handle empty flight data
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
            0,
        )

    # Combine direct and indirect flights
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

    # Calculate the number of stopovers
    stops = len(first_flight["flights"]) - 1

    # Create the initial FlightData object
    cheapest_flight = FlightData(
        lowest_price,
        origin,
        destination,
        out_date,
        return_date,
        stops,
    )

    # Compare all available flights
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

            # Calculate stopovers for the cheapest flight
            stops = len(flight["flights"]) - 1

            cheapest_flight = FlightData(
                lowest_price,
                origin,
                destination,
                out_date,
                return_date,
                stops,
            )

            print(
                f"Lowest price to "
                f"{destination} "
                f"is GBP {lowest_price}"
            )

    return cheapest_flight