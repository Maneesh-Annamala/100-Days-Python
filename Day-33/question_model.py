class Question:
    """Represents a single quiz question."""

    def __init__(self, q_text, q_answer):
        """Initialize a question with its text and correct answer."""

        # Stores the question text
        self.text = q_text

        # Stores the correct answer
        self.answer = q_answer