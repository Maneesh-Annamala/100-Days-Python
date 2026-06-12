from turtle import Turtle
import random

class Food(Turtle):
    """Represents the food eaten by the snake."""

    def __init__(self):
        super().__init__()

        # Configure food appearance
        self.shape("circle")
        self.color("red")
        self.penup()

        # Make food smaller
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)

        # Place food at random position
        self.food_position()

    def food_position(self):
        """Move food to a random location."""

        random_x = random.randint(-270, 270)
        random_y = random.randint(-270, 270)

        self.goto(random_x, random_y)