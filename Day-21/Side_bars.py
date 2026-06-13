from turtle import Turtle

class Bar(Turtle):
    """Represents a player's paddle."""

    def __init__(self, position):
        super().__init__()

        self.shape("square")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.color("white")
        self.penup()

        self.goto(position)

    def go_up(self):
        """Move paddle upward."""

        new_y = self.ycor() + 30
        self.goto(self.xcor(), new_y)

    def go_down(self):
        """Move paddle downward."""

        new_y = self.ycor() - 30
        self.goto(self.xcor(), new_y)