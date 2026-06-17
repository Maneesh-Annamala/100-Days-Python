import turtle
from turtle import Turtle, Screen
import pandas as pd

# Store correct and missed states
corrected_states = []
unanswered_states = []

# Create turtle for writing state names
tim = Turtle()
tim.penup()
tim.hideturtle()

# Configure screen
screen = Screen()
screen.title("U.S. States Quiz")

# Load map image
image = "blank_states_img.gif"
screen.addshape(image)
screen.bgpic(image)

# Load CSV data
data = pd.read_csv("50_states.csv")

# Convert states column to list
states = data.state.to_list()

# Run game until all states are guessed
while len(corrected_states) < 50:

    answer_state = screen.textinput(
        title=f"{len(corrected_states)}/50 Correct States",
        prompt="Enter the state:")

    # Exit game
    if answer_state == "Exit":
        break

    answer_state = answer_state.title()

    # Check correct answer
    if (answer_state in states and answer_state not in corrected_states):

        state_data = data[data.state == answer_state]

        tim.goto(
            state_data.x.item(),
            state_data.y.item()
        )

        tim.write(
            answer_state,
            font=("Arial", 10, "bold")
        )

        corrected_states.append(answer_state)

# Find unanswered states
for state in states:

    if state not in corrected_states:
        unanswered_states.append(state)

# Display missed states
print("Unanswered states:")

for state in unanswered_states:
    print(state)

#if we wanted to create another csv file with missed states 

# new_data = pd.DataFrame(unanswered_states)
# new_data.to_csv("states_to_learn.csv")
