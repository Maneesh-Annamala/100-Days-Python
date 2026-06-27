from tkinter import *
from quiz_brain import QuizBrain

# Background color of the application
THEME_COLOR = "#375362"


class QuizInterface:
    """Creates and manages the Quiz GUI."""

    def __init__(self, quiz):
        """Initialize all GUI components."""

        # QuizBrain object
        self.quiz = quiz

        # Main application window
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(
            padx=20,
            pady=20,
            bg=THEME_COLOR
        )

        # Score label
        self.score_text = Label(
            text="Score: 0",
            bg=THEME_COLOR,
            fg="white"
        )
        self.score_text.grid(row=0, column=1)

        # Canvas to display questions
        self.canvas = Canvas(
            width=300,
            height=250,
            bg="white",
            highlightthickness=0
        )

        # Question text
        self.new_question = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Hello There",
            font=("Arial", 20, "italic")
        )

        self.canvas.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=50
        )

        # True button image
        right_image = PhotoImage(file="images/true.png")

        # True button
        self.right_button = Button(
            image=right_image,
            highlightthickness=0,
            command=self.true_answer
        )
        self.right_button.grid(row=2, column=0)

        # Prevent image from being garbage collected
        self.right_button.image = right_image

        # False button image
        wrong_image = PhotoImage(file="images/false.png")

        # False button
        self.wrong_button = Button(
            image=wrong_image,
            highlightthickness=0,
            command=self.false_answer
        )
        self.wrong_button.grid(row=2, column=1)

        # Prevent image from being garbage collected
        self.wrong_button.image = wrong_image

        # Display the first question
        self.question_change()

        self.window.mainloop()

    def question_change(self):
        """Display the next question."""

        # Reset canvas color
        self.canvas.config(bg="white")

        if self.quiz.still_has_questions():

            # Get next question
            q_text = self.quiz.next_question()

            # Update score
            self.score_text.config(
                text=f"Score: {self.quiz.score}"
            )

            # Display question
            self.canvas.itemconfig(
                self.new_question,
                text=q_text
            )

        else:

            # Quiz completed
            self.canvas.itemconfig(
                self.new_question,
                text="Game Over\n\nYou've completed the quiz!"
            )

            # Disable answer buttons
            self.right_button.config(state="disabled")
            self.wrong_button.config(state="disabled")

    def true_answer(self):
        """Handle True button click."""

        is_right = self.quiz.check_answer("True")
        self.feedback(is_right)

    def false_answer(self):
        """Handle False button click."""

        is_right = self.quiz.check_answer("False")
        self.feedback(is_right)

    def feedback(self, is_right):
        """Show answer feedback before displaying the next question."""

        # Green for correct answer
        if is_right:
            self.canvas.config(bg="green")

        # Red for wrong answer
        else:
            self.canvas.config(bg="red")

        # Wait 1 second before next question
        self.window.after(
            1000,
            func=self.question_change
        )