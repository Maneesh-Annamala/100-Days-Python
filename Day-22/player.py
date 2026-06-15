from turtle import Turtle

# Player settings
STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    """Represents the player turtle."""

    def __init__(self):
        super().__init__()

        self.shape("turtle")
        self.penup()

        # Move player to starting position
        self.reset_position()

        # Face upward
        self.setheading(90)

    def reset_position(self):
        """Return player to starting position."""

        self.goto(STARTING_POSITION)

    def move(self):
        """Move player forward."""

        self.forward(MOVE_DISTANCE)