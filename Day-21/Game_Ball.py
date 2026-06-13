from turtle import Turtle

class Ball(Turtle):
    """Represents the pong ball."""

    def __init__(self):
        super().__init__()

        # Configure ball appearance
        self.shape("circle")
        self.color("white")
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.penup()

        # Ball movement values
        self.x_num = 10
        self.y_num = 10

        # Control game speed
        self.move_speed = 0.1

    def move_the_ball(self):
        """Move ball continuously."""

        new_x = self.xcor() + self.x_num
        new_y = self.ycor() + self.y_num

        self.goto(new_x, new_y)

    def l_bounce(self):
        """Bounce ball from top and bottom walls."""

        self.y_num *= -1

    def r_bounce(self):
        """Bounce ball from paddles."""

        self.x_num *= -1

        # Increase game speed
        self.move_speed *= 0.9

    def reset_position(self):
        """Reset ball after a point is scored."""

        self.goto(0, 0)

        self.move_speed = 0.1

        self.r_bounce()