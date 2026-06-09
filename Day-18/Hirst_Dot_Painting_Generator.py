import colorgram
import random
import turtle

# Extract colors from image
colors = colorgram.extract('harsh.jpg', 30)

colors_rgb = []

# Convert extracted colors into RGB tuples
for i in colors:
    r = i.rgb.r
    g = i.rgb.g
    b = i.rgb.b

    result = (r, g, b)
    colors_rgb.append(result)

# Enable RGB color mode
turtle.colormode(255)

# Create turtle object
tim = turtle.Turtle()

tim.hideturtle()
tim.penup()
tim.speed(10)

# Move turtle to starting position
tim.setheading(225)
tim.forward(300)
tim.setheading(0)

# Draw 10x10 dot painting
for i in range(1, 101):

    # Draw colored dot
    tim.dot(20, random.choice(colors_rgb))

    tim.forward(50)

    # Move to next row after every 10 dots
    if i % 10 == 0:
        tim.left(90)
        tim.forward(50)
        tim.left(90)
        tim.forward(500)
        tim.setheading(0)

# Keep screen open
screen = turtle.Screen()
screen.exitonclick()