from turtle import Turtle

# Font settings for scoreboard
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    """Handles level display and game over message."""

    def __init__(self):
        super().__init__()

        # Initialize level
        self.level = 0

        # Configure scoreboard turtle
        self.penup()
        self.hideturtle()

        # Position scoreboard
        self.goto(-280, 260)

        self.level_up()

    def level_up(self):
        """Display current level."""

        self.clear()

        self.write(
            f"Level: {self.level}",
            align="left",
            font=FONT
        )

    def increase_level(self):
        """Increase level by one."""

        self.level += 1

    def game_over(self):
        """Display game over message."""

        self.goto(0, 0)

        self.write(
            "GAME OVER!",
            align="center",
            font=FONT
        )