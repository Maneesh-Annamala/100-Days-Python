from turtle import Turtle

class Score(Turtle):
    """Handles score display and game over message."""

    def __init__(self):
        super().__init__()

        # Set scoreboard position and style
        self.penup()
        self.goto(0, 270)
        self.color("white")
        self.hideturtle()

        # Initialize score
        self.score = 0

        self.display()

    def display(self):
        """Display current score."""

        self.write(
            f"Score: {self.score}",
            align="center",
            font=("Arial", 20, "normal")
        )

    def collision_message(self):
        """Display game over message."""

        self.goto(0, 0)

        self.write(
            "Game Over",
            align="center",
            font=("Arial", 20, "normal")
        )

    def increase_score(self):
        """Update scoreboard after scoring."""

        self.clear()
        self.display()