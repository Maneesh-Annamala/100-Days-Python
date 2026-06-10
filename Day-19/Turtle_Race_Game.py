from turtle import Turtle, Screen
import random

# Control race state
is_race_on = False

# Create screen
screen = Screen()
screen.setup(height=400, width=500)


# Available turtle colors and positions
colors = ["red", "blue", "orange", "yellow", "deep pink", "black"]
y_sides = [-100, -60, -20, 20, 60, 100]

# Ask user to choose a turtle color
user_color = screen.textinput(
    title="Turtle Race",
    prompt="Choose your color: "
)
while user_color not in colors:
    print("We don't have turtle with that colore.Please choose another color")
    user_color = screen.textinput(
    title="Turtle Race",
    prompt="Choose your color: "
    )

new_turtles = []

# Start race if user entered a color
if user_color:
    is_race_on = True

# Create turtles
for i in range(0, 6):
    tim = Turtle(shape="turtle")
    tim.color(colors[i])
    tim.penup()
    tim.goto(x=-230, y=y_sides[i])

    new_turtles.append(tim)

# Run race
while is_race_on:

    for tims in new_turtles:

        # Check winner
        if tims.xcor() >= 230:

            is_race_on = False

            turtle_color = tims.pencolor()

            if turtle_color == user_color:
                print(f"You won! {turtle_color} has reached the goal first")

            else:
                print(f"You Lost! {turtle_color} has reached the goal first")

        # Move turtle forward randomly
        tims.forward(random.randint(0, 10))

# Keep screen open
screen.exitonclick()