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
        with open("data.txt", "r") as file:
            self.highscore = int(file.read())

        # Initialize score
        self.score = 0

        self.display()
    def display(self):
        """Display current score."""

        self.write(
            f"Score: {self.score} Highscore: {self.highscore}",
            align="center",
            font=("Arial", 20, "normal")
        )

    def reset_score(self):
        """Reset score."""
        self.clear()
        if self.score > self.highscore:
            self.highscore = self.score
            with open("data.txt", "w") as file:
                file.write(f"{self.highscore}")
        self.score = 0
        self.display()

    def increase_score(self):
        """Update scoreboard after scoring."""

        self.clear()
        self.display()