# Simple Snake game using the Pyxel library
from collections import deque, namedtuple
import pyxel

# Pyxel game engine

Point = namedtuple("Point", ["x", "y"])

# Tuple class representing a point (x, y)

# Main game class that encapsulates snake state and game loop
class Snake:

    def __init__(self):
        # Initialize a 40×50 window at 5 frames per second
        pyxel.init(40, 50, fps=5)
        # Initial movement direction: right
        self.direction = Point(1, 0)
        # Use deque to store snake segments
        self.snake = deque()
        # Start with one segment at position (5, 5)
        self.snake.append(Point(5, 5))
        # Start the main game loop: update then draw each frame
        pyxel.run(self.update, self.draw)

    def update(self):
        # Determine the current head position
        head = self.snake[0]
        # Add a new head segment in the current direction
        self.snake.appendleft(Point(head.x + self.direction.x,
                                    head.y + self.direction.y))

    def draw(self):
        # Clear the screen with palette color 3
        pyxel.cls(3)
        # Draw each segment of the snake in color 7
        for x, y in self.snake:
            pyxel.pset(x, y, 7)

Snake()