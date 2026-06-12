from turtle import Screen
import time
from snake import Snake
from TurtleFood import Food
from Scoreboard import Score

# Create game screen
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.tracer(0)

# Create game objects
scoreboard = Score()
food = Food()
snakes = Snake()

# Set keyboard controls
screen.listen()
screen.onkey(snakes.up, "Up")
screen.onkey(snakes.down, "Down")
screen.onkey(snakes.right, "Right")
screen.onkey(snakes.left, "Left")

# Run game loop
is_game_on = True

while is_game_on:

    # Refresh screen and move snake
    screen.update()
    time.sleep(0.1)
    snakes.move()

    # Check food collision
    if snakes.head.distance(food) < 15:
        food.food_position()
        scoreboard.score += 1
        snakes.extend()
        scoreboard.increase_score()

    # Check wall collision
    if (
        snakes.head.xcor() > 280
        or snakes.head.xcor() < -280
        or snakes.head.ycor() > 280
        or snakes.head.ycor() < -280
    ):
        is_game_on = False
        scoreboard.collision_message()

    # Check self collision
    for segments in snakes.new_segments[1:]:
        if snakes.head.distance(segments) < 10:
            is_game_on = False
            scoreboard.collision_message()

# Keep screen open
screen.exitonclick()