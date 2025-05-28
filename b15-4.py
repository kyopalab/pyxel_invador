# Simple Snake game using the Pyxel library
# Controls the snake moving automatically and draws it segment by segment
from collections import deque, namedtuple
import pyxel

# Convenience tuple for 2D coordinates
Point = namedtuple("Point", ["x", "y"])

# Main game class encapsulating snake state and game loop
class Snake:

    def __init__(self):
        # Initialize a 40×50 window with 5 frames per second
        pyxel.init(40, 50, fps=5)
        # Initial movement direction: right
        self.direction = Point(1, 0)
        # Use deque to represent the snake segments
        self.snake = deque()
        # Start the snake with a single segment at (5,5)
        self.snake.append(Point(5, 5))
        # Start the main loop: call update() then draw() every frame
        pyxel.run(self.update, self.draw)

    def update(self):
        # Calculate the new head position based on current direction
        head = self.snake[0]
        # Add new head to the front of the deque
        self.snake.appendleft(Point(head.x + self.direction.x,
                                    head.y + self.direction.y))
        # Remove the tail segment every 5th frame to control speed
        if (pyxel.frame_count % 5 != 0):
            self.snake.pop()

    def draw(self):
        # Clear screen with palette color 3
        pyxel.cls(3)
        # Draw each segment: head in color 7, body in color 11
        for i, point in enumerate(self.snake):
            if i == 0:
                color = 7
            else:
                color = 11
            pyxel.pset(point.x, point.y, color)

Snake()