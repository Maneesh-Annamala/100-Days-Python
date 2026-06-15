from turtle import Turtle
import random

# Available car colors
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]

# Initial car movement speed
STARTING_MOVE_DISTANCE = 5

# Speed increase after each level
MOVE_INCREMENT = 5


class CarManager:
    """Creates and controls all cars in the game."""

    def __init__(self):

        # Store all cars
        self.all_cars = []

        # Current car movement speed
        self.car_speed = STARTING_MOVE_DISTANCE

    def create_car(self):
        """Randomly create new cars."""

        x = random.randint(1, 6)

        if x == 1:

            new_car = Turtle("square")

            new_car.penup()
            new_car.color(random.choice(COLORS))

            # Stretch square into rectangle
            new_car.shapesize(
                stretch_wid=1,
                stretch_len=2
            )

            random_y = random.randint(-250, 250)

            new_car.goto(300, random_y)

            self.all_cars.append(new_car)

    def move_cars(self):
        """Move all cars across the screen."""

        for car in self.all_cars:
            car.backward(self.car_speed)

    def increase_speed(self):
        """Increase car movement speed."""

        self.car_speed += MOVE_INCREMENT