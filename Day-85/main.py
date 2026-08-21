import tkinter as tk


WIDTH = 800
HEIGHT = 600

PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
PADDLE_SPEED = 25

BALL_SIZE = 18
BALL_START_SPEED_X = 4
BALL_START_SPEED_Y = -4

BRICK_ROWS = 5
BRICK_COLUMNS = 8
BRICK_WIDTH = 80
BRICK_HEIGHT = 25
BRICK_GAP = 10
BRICK_START_X = 40
BRICK_START_Y = 70


class BreakoutGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Beginner Breakout")

        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg="black"
        )
        self.canvas.pack()

        self.score = 0
        self.lives = 3
        self.game_over = False

        self.score_text = self.canvas.create_text(
            70,
            25,
            text="Score: 0",
            fill="white",
            font=("Arial", 16)
        )

        self.lives_text = self.canvas.create_text(
            WIDTH - 70,
            25,
            text="Lives: 3",
            fill="white",
            font=("Arial", 16)
        )

        self.create_paddle()
        self.create_ball()
        self.create_bricks()

        self.root.bind("<Left>", self.move_paddle_left)
        self.root.bind("<Right>", self.move_paddle_right)
        self.root.bind("<space>", self.restart_game)

        self.move_ball()

    def create_paddle(self):
        paddle_x = (WIDTH - PADDLE_WIDTH) / 2
        paddle_y = HEIGHT - 50

        self.paddle = self.canvas.create_rectangle(
            paddle_x,
            paddle_y,
            paddle_x + PADDLE_WIDTH,
            paddle_y + PADDLE_HEIGHT,
            fill="dodger blue"
        )

    def create_ball(self):
        ball_x = (WIDTH - BALL_SIZE) / 2
        ball_y = HEIGHT - 85

        self.ball = self.canvas.create_oval(
            ball_x,
            ball_y,
            ball_x + BALL_SIZE,
            ball_y + BALL_SIZE,
            fill="white"
        )

        self.ball_speed_x = BALL_START_SPEED_X
        self.ball_speed_y = BALL_START_SPEED_Y

    def create_bricks(self):
        self.bricks = []

        colors = [
            "red",
            "orange",
            "yellow",
            "lime green",
            "cyan"
        ]

        for row in range(BRICK_ROWS):
            for column in range(BRICK_COLUMNS):
                x1 = BRICK_START_X + column * (BRICK_WIDTH + BRICK_GAP)
                y1 = BRICK_START_Y + row * (BRICK_HEIGHT + BRICK_GAP)
                x2 = x1 + BRICK_WIDTH
                y2 = y1 + BRICK_HEIGHT

                brick = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=colors[row],
                    outline="black"
                )

                self.bricks.append(brick)

    def move_paddle_left(self, event):
        if self.game_over:
            return

        x1, _, _, _ = self.canvas.coords(self.paddle)

        if x1 > 0:
            self.canvas.move(
                self.paddle,
                -PADDLE_SPEED,
                0
            )

    def move_paddle_right(self, event):
        if self.game_over:
            return

        _, _, x2, _ = self.canvas.coords(self.paddle)

        if x2 < WIDTH:
            self.canvas.move(
                self.paddle,
                PADDLE_SPEED,
                0
            )

    def move_ball(self):
        if self.game_over:
            return

        self.canvas.move(
            self.ball,
            self.ball_speed_x,
            self.ball_speed_y
        )

        x1, y1, x2, y2 = self.canvas.coords(self.ball)

        if x1 <= 0 or x2 >= WIDTH:
            self.ball_speed_x = -self.ball_speed_x

        if y1 <= 0:
            self.ball_speed_y = -self.ball_speed_y

        if y2 >= HEIGHT:
            self.lose_life()
            return

        self.check_paddle_collision()
        self.check_brick_collision()

        self.root.after(16, self.move_ball)

    def check_paddle_collision(self):
        ball_coords = self.canvas.coords(self.ball)
        paddle_coords = self.canvas.coords(self.paddle)

        if (
            self.is_colliding(ball_coords, paddle_coords)
            and self.ball_speed_y > 0
        ):
            self.ball_speed_y = -self.ball_speed_y

    def check_brick_collision(self):
        ball_coords = self.canvas.coords(self.ball)

        for brick in self.bricks:
            brick_coords = self.canvas.coords(brick)

            if self.is_colliding(ball_coords, brick_coords):
                self.canvas.delete(brick)
                self.bricks.remove(brick)

                self.ball_speed_y = -self.ball_speed_y

                self.score += 10

                self.canvas.itemconfig(
                    self.score_text,
                    text=f"Score: {self.score}"
                )

                if len(self.bricks) == 0:
                    self.win_game()

                break

    def is_colliding(self, object1, object2):
        obj1_x1, obj1_y1, obj1_x2, obj1_y2 = object1
        obj2_x1, obj2_y1, obj2_x2, obj2_y2 = object2

        return (
            obj1_x2 >= obj2_x1
            and obj1_x1 <= obj2_x2
            and obj1_y2 >= obj2_y1
            and obj1_y1 <= obj2_y2
        )

    def lose_life(self):
        self.lives -= 1

        self.canvas.itemconfig(
            self.lives_text,
            text=f"Lives: {self.lives}"
        )

        if self.lives == 0:
            self.end_game(
                "Game Over! Press Space to restart"
            )
        else:
            self.reset_ball_and_paddle()
            self.root.after(800, self.move_ball)

    def reset_ball_and_paddle(self):
        self.canvas.coords(
            self.paddle,
            (WIDTH - PADDLE_WIDTH) / 2,
            HEIGHT - 50,
            (WIDTH + PADDLE_WIDTH) / 2,
            HEIGHT - 50 + PADDLE_HEIGHT
        )

        self.canvas.coords(
            self.ball,
            (WIDTH - BALL_SIZE) / 2,
            HEIGHT - 85,
            (WIDTH + BALL_SIZE) / 2,
            HEIGHT - 85 + BALL_SIZE
        )

        self.ball_speed_x = BALL_START_SPEED_X
        self.ball_speed_y = BALL_START_SPEED_Y

    def win_game(self):
        self.end_game(
            "You Win! Press Space to restart"
        )

    def end_game(self, message):
        self.game_over = True

        self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2,
            text=message,
            fill="white",
            font=("Arial", 24),
            tag="end_message"
        )

    def restart_game(self, event):
        if not self.game_over:
            return

        self.canvas.delete("all")

        self.score = 0
        self.lives = 3
        self.game_over = False

        self.score_text = self.canvas.create_text(
            70,
            25,
            text="Score: 0",
            fill="white",
            font=("Arial", 16)
        )

        self.lives_text = self.canvas.create_text(
            WIDTH - 70,
            25,
            text="Lives: 3",
            fill="white",
            font=("Arial", 16)
        )

        self.create_paddle()
        self.create_ball()
        self.create_bricks()

        self.move_ball()


if __name__ == "__main__":
    root = tk.Tk()
    game = BreakoutGame(root)
    root.mainloop()