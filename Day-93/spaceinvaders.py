import turtle
import random
import time


# Screen setup
screen = turtle.Screen()
screen.title("Space Invaders")
screen.bgcolor("black")
screen.setup(width=800, height=700)
screen.tracer(0)

# Player
player = turtle.Turtle()
player.shape("triangle")
player.color("cyan")
player.penup()
player.setheading(90)
player.goto(0, -300)

player_speed = 20

# Bullet
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.shapesize(stretch_wid=0.5, stretch_len=0.2)
bullet.penup()
bullet.hideturtle()

bullet_speed = 20
bullet_state = "ready"

# Aliens
aliens = []
alien_colors = ["red", "orange", "green", "purple"]

for row in range(4):
    for column in range(8):
        alien = turtle.Turtle()
        alien.shape("turtle")
        alien.color(alien_colors[row])
        alien.penup()
        x = -280 + column * 80
        y = 250 - row * 60
        alien.goto(x, y)
        aliens.append(alien)
# Score
score = 0

score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-370, 310)

score_display.write(
    f"Score: {score}",
    align="left",
    font=("Arial", 16, "normal"))

# Lives
lives = 3

lives_display = turtle.Turtle()
lives_display.color("white")
lives_display.penup()
lives_display.hideturtle()
lives_display.goto(250, 310)

lives_display.write(
    f"Lives: {lives}",
    align="left",
    font=("Arial", 16, "normal"))

# Player movement
def move_left():
    x = player.xcor()
    if x > -370:
        player.setx(x - player_speed)


def move_right():
    x = player.xcor()
    if x < 370:
        player.setx(x + player_speed)

# Shooting
def shoot():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(),
            player.ycor() + 20)
        bullet.showturtle()

# Collision detection

def is_collision(t1, t2):
    distance = t1.distance(t2)
    if distance < 25:
        return True
    return False

# Keyboard controls
screen.listen()

screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(shoot, "space")

# Alien movement

alien_direction = 1
alien_speed = 2

# Game Over
game_over = False

game_over_display = turtle.Turtle()
game_over_display.color("white")
game_over_display.penup()
game_over_display.hideturtle()

while True:
    screen.update()
    # Move bullet
    if bullet_state == "fire":
        y = bullet.ycor()
        bullet.sety(y + bullet_speed)
        # Bullet reached top
        if bullet.ycor() > 340:
            bullet.hideturtle()
            bullet_state = "ready"
    # Move aliens
    move_down = False
    for alien in aliens:
        x = alien.xcor()
        # Hit screen boundary
        if x > 370 or x < -370:
            move_down = True
    if move_down:
        alien_direction *= -1
        for alien in aliens:
            alien.sety(alien.ycor() - 20)
    # Move aliens horizontally
    for alien in aliens:
        alien.setx(alien.xcor() +
            alien_speed * alien_direction)
    # Bullet collision
    for alien in aliens:
        if bullet_state == "fire":
            if is_collision(bullet, alien):
                bullet.hideturtle()
                bullet_state = "ready"
                alien.hideturtle()
                aliens.remove(alien)
                score += 10
                score_display.clear()
                score_display.write(
                    f"Score: {score}",
                    align="left",
                    font=("Arial", 16, "normal")
                )
                break
    # Alien reaches player
    for alien in aliens:
        if alien.ycor() < -260:
            lives -= 1
            lives_display.clear()

            lives_display.write(
                f"Lives: {lives}",
                align="left",
                font=("Arial", 16, "normal")
            )

            alien.hideturtle()
            aliens.remove(alien)

            break
    # Alien collision with player
    for alien in aliens:
        if is_collision(player, alien):
            lives = 0
            lives_display.clear()
            lives_display.write(
                "Lives: 0",
                align="left",
                font=("Arial", 16, "normal")
            )
            break
    if len(aliens) == 0:
        game_over_display.goto(0, 0)
        game_over_display.write(
            "YOU WIN!",
            align="center",
            font=("Arial", 36, "bold")
        )
        break
    
    # Lose condition
    if lives <= 0:

        game_over_display.goto(0, 0)

        game_over_display.write(
            "GAME OVER",
            align="center",
            font=("Arial", 36, "bold")
        )
        break
    time.sleep(0.02)
screen.mainloop()