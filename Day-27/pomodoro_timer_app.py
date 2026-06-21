from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# Timer durations (in minutes)
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# Keeps track of completed sessions
reps = 0

# Stores the currently running timer reference
timer_run = None


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    """Reset the timer and restore the application to its initial state."""

    global reps

    # Cancel the currently running timer
    window.after_cancel(timer_run)

    # Reset timer display
    canvas.itemconfig(timer, text="00:00")

    # Reset heading text
    timer_text.config(text="Timer", fg=GREEN)

    # Clear completed session marks
    tick_mark.config(text="")

    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    """Start work, short break, or long break session."""

    global reps

    reps += 1

    # Work sessions
    if reps == 1 or reps == 3 or reps == 5 or reps == 7:
        timer_text.config(text="Work Timer", bg=YELLOW, fg=GREEN)
        count_down(WORK_MIN * 60)

    # Short break sessions
    elif reps == 2 or reps == 4 or reps == 6:
        timer_text.config(text="Short Break", bg=YELLOW, fg=PINK)
        count_down(SHORT_BREAK_MIN * 60)

    # Long break session
    elif reps == 8:
        timer_text.config(text="Long Break", bg=YELLOW, fg=RED)
        count_down(LONG_BREAK_MIN * 60)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    """Handle countdown logic and automatically switch sessions."""

    global reps

    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    # Update timer text on canvas
    canvas.itemconfig(timer, text=f"{count_min}:{count_sec}")

    if count > 0:

        global timer_run

        # Schedule next countdown after 1 second
        timer_run = window.after(1000, count_down, count - 1)

    else:

        # Automatically start next session
        start_timer()

        check_marks = ""

        # Add a checkmark after every completed work session
        work_sessions = math.floor(reps/2)
        check_marks = "✔" * work_sessions

        tick_mark.config(text=check_marks)


# ---------------------------- UI SETUP ------------------------------- #

# Create main application window
window = Tk()

window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Timer heading
timer_text = Label(
    text="Timer",
    bg=YELLOW,
    fg=GREEN,
    font=(FONT_NAME, 30, "bold")
)
timer_text.grid(row=1, column=2)

# Canvas containing tomato image and timer display
canvas = Canvas(
    width=200,
    height=224,
    bg=YELLOW,
    highlightthickness=0
)

photo = PhotoImage(file="tomato.png")

canvas.create_image(100, 112, image=photo)

timer = canvas.create_text(
    102,
    130,
    text="00:00",
    fill="white",
    font=(FONT_NAME, 35, "bold")
)

canvas.grid(row=2, column=2)

# Start button
start_button = Button(
    text="Start",
    highlightthickness=0,
    command=start_timer
)
start_button.grid(row=3, column=1)

# Reset button
reset_button = Button(
    text="Reset",
    highlightthickness=0,
    command=reset_timer
)
reset_button.grid(row=3, column=3)

# Displays completed work sessions
tick_mark = Label(
    bg=YELLOW,
    fg=GREEN
)
tick_mark.grid(row=4, column=2)

window.mainloop()