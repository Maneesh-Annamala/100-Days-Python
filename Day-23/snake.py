from turtle import Turtle

# Starting snake positions
POSITIONS = [(0, 0), (-20, 0), (-40, 0)]

# Movement settings
MOVING_POSITIONS = 20

UP = 90
DOWN = 270
RIGHT = 0
LEFT = 180


class Snake:
    """Represents the snake and its movement."""

    def __init__(self):
        self.new_segments = []

        # Create initial snake
        self.creation()

        # Store snake head reference
        self.head = self.new_segments[0]

    def creation(self):
        """Create the starting snake."""

        for position in POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        """Add a new segment to the snake."""

        tim = Turtle()
        tim.color("white")
        tim.penup()
        tim.shape("square")
        tim.goto(position)

        self.new_segments.append(tim)

    def reset_snake(self):
        """Reset the snake to its initial position."""
        for seg in self.new_segments:
            seg.goto(1000, 1000)
        self.new_segments.clear()
        self.creation()
        self.head = self.new_segments[0]

    def extend(self):
        """Increase snake length by one segment."""

        self.add_segment(self.new_segments[-1].position())

    def move(self):
        """Move the snake forward."""

        # Move body segments
        for seg in range(len(self.new_segments) - 1, 0, -1):

            new_x = self.new_segments[seg - 1].xcor()
            new_y = self.new_segments[seg - 1].ycor()

            self.new_segments[seg].goto(new_x, new_y)

        # Move head forward
        self.head.forward(MOVING_POSITIONS)

    def up(self):
        """Move snake upward."""

        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        """Move snake downward."""

        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def right(self):
        """Move snake right."""

        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def left(self):
        """Move snake left."""

        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)