# Simple Snake game using Pyxel that moves a single point
from collections import namedtuple
import pyxel

# Pyxel game library for window management and drawing

Point = namedtuple("Point", ["x", "y"])

# A lightweight 2D coordinate container

# Main application class encapsulating snake logic
class Snake:

    def __init__(self):
        # Initialize a 40×50 window titled "Snake!" at 5 FPS
        pyxel.init(40, 50, fps=5)
        # Starting movement direction: right
        self.direction = Point(1, 0)
        # Starting position of snake head at (5,5)
        self.snake = Point(5, 5)
        # Start the game loop: call update() then draw() every frame
        pyxel.run(self.update, self.draw)

    def update(self):
        # Move snake head by adding direction to its coordinates
        self.snake = Point(self.snake.x + self.direction.x,
                           self.snake.y + self.direction.y)

    def draw(self):
        # Clear screen with color 3
        pyxel.cls(3)
        # Draw the snake head in color 7
        pyxel.pset(self.snake.x, self.snake.y, 7)

Snake()