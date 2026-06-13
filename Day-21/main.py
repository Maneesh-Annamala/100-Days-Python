from turtle import Screen
from Side_bars import Bar
from Game_Ball import Ball
from scoreboard import Score
import time

# Create game screen
screen = Screen()
screen.bgcolor("black")
screen.setup(height=600, width=800)
screen.title("Pong")

# Turn off automatic screen updates
screen.tracer(0)

# Create paddles, ball and scoreboard
right_paddle = Bar((350, 0))
left_paddle = Bar((-350, 0))
balls = Ball()
score = Score()

# Set keyboard controls
screen.listen()

screen.onkey(right_paddle.go_up, "Up")
screen.onkey(right_paddle.go_down, "Down")

screen.onkey(left_paddle.go_up, "w")
screen.onkey(left_paddle.go_down, "s")

# Start game loop
game_on = True

while game_on:

    # Refresh screen
    screen.update()

    # Control ball movement speed
    time.sleep(balls.move_speed)

    # Move ball
    balls.move_the_ball()

    # Detect collision with top and bottom walls
    if balls.ycor() > 280 or balls.ycor() < -280:
        balls.l_bounce()

    # Detect collision with paddles
    if (
        right_paddle.distance(balls) < 50
        and balls.xcor() > 320
    ) or (
        left_paddle.distance(balls) < 50
        and balls.xcor() < -320
    ):
        balls.r_bounce()

    # Right paddle missed the ball
    if balls.xcor() > 380:
        balls.reset_position()
        score.l_point()

    # Left paddle missed the ball
    if balls.xcor() < -380:
        balls.reset_position()
        score.r_point()

# Keep screen open
screen.exitonclick()