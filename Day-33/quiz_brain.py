import html

class QuizBrain:
    """Handles the quiz logic such as questions, score, and answer checking."""

    def __init__(self, q_list):
        """Initialize the quiz with a list of questions."""

        # Keeps track of current question number
        self.question_number = 0

        # Stores the user's score
        self.score = 0

        # Stores all quiz questions
        self.question_list = q_list

        # Stores the current question object
        self.current_question = None

    def still_has_questions(self):
        """Return True if there are questions remaining."""

        return self.question_number < len(self.question_list)

    def next_question(self):
        """Retrieve the next question from the question list."""

        # Get the current question
        self.current_question = self.question_list[self.question_number]

        # Move to the next question
        self.question_number += 1

        # Convert HTML entities into readable text
        q_text = html.unescape(self.current_question.text)

        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer):
        """Check whether the user's answer is correct."""

        # Get the correct answer
        correct_answer = self.current_question.answer

        # Compare answers
        if user_answer.lower() == correct_answer.lower():

            # Increase score for correct answer
            self.score += 1

            return True

        else:
            return False