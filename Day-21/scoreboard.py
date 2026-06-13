from turtle import Turtle

class Score(Turtle):
    """Handles score display."""

    def __init__(self):
        super().__init__()

        self.color("white")
        self.penup()
        self.hideturtle()

        self.l_score = 0
        self.r_score = 0

        self.increase_score()

    def increase_score(self):
        """Refresh scoreboard."""

        self.clear()

        self.goto(-100, 200)
        self.write(
            self.l_score,
            align="center",
            font=("Courier", 50, "normal")
        )

        self.goto(100, 200)
        self.write(
            self.r_score,
            align="center",
            font=("Courier", 50, "normal")
        )

    def l_point(self):
        """Increase left player's score."""

        self.l_score += 1
        self.increase_score()

    def r_point(self):
        """Increase right player's score."""

        self.r_score += 1
        self.increase_score()