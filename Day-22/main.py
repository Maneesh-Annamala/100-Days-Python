import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

FINISH_LINE_Y = 280

# Create game screen
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

# Create game objects
player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

# Set keyboard controls
screen.listen()
screen.onkey(player.move, "Up")

# Start game loop
game_is_on = True

while game_is_on:

    # Control game speed
    time.sleep(0.1)

    # Refresh screen
    screen.update()

    # Generate and move cars
    car_manager.create_car()
    car_manager.move_cars()

    # Detect collision between player and cars
    for car in car_manager.all_cars:

        if player.distance(car) < 20:
            game_is_on = False
            scoreboard.game_over()

    # Detect successful crossing
    if player.ycor() > FINISH_LINE_Y:

        # Reset player position
        player.reset_position()

        # Increase level
        scoreboard.increase_level()
        scoreboard.level_up()

        # Increase car speed
        car_manager.increase_speed()

# Keep screen open
screen.exitonclick()