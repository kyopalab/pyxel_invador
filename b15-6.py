"""Snake implemented with pyxel.

This is the game of snake in pyxel version!

Try and collect the tasty apples without running
into the side or yourself.

Controls are the arrow keys ← ↑ → ↓

Q: Quit the game
R: Restart the game

Created by Marcus Croucher in 2018.
"""

from collections import deque, namedtuple
from random import randint

import pyxel

Point = namedtuple("Point", ["x", "y"])  # Convenience class for coordinates


#############
# Constants #
#############

COL_BACKGROUND = 3
COL_BODY = 11
COL_HEAD = 7
COL_DEATH = 8
COL_APPLE = 8

TEXT_DEATH = ["GAME OVER", "(Q)UIT", "(R)ESTART"]
COL_TEXT_DEATH = 0
HEIGHT_DEATH = 5

WIDTH = 40
HEIGHT = 50

HEIGHT_SCORE = pyxel.FONT_HEIGHT
COL_SCORE = 6
COL_SCORE_BACKGROUND = 5

UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)

START = Point(5, 5 + HEIGHT_SCORE)


###################
# The game itself #
###################


class Snake:
    """The class that sets up and runs the game."""

    def __init__(self):
        """Initiate pyxel, set up initial game variables, and run."""
        pyxel.init(WIDTH, HEIGHT, fps=2)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        """Initiate key variables (direction, snake, score, death flag, etc.)"""
        self.direction = RIGHT
        self.snake = deque()
        self.snake.append(START)
        self.death = False  # Track whether the game has ended

    ##############
    # Game logic #
    ##############

    def update(self):
        """Update logic of game. Moves snake, checks death, handles Q/R."""
        if not self.death:
            self.update_direction()
            self.update_snake()
            self.check_death()

        # Quit or restart always available
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

    def update_direction(self):
        """Watch the arrow keys and change direction (no 180° turn)."""
        if pyxel.btn(pyxel.KEY_UP) and self.direction is not DOWN:
            self.direction = UP
        elif pyxel.btn(pyxel.KEY_DOWN) and self.direction is not UP:
            self.direction = DOWN
        elif pyxel.btn(pyxel.KEY_LEFT) and self.direction is not RIGHT:
            self.direction = LEFT
        elif pyxel.btn(pyxel.KEY_RIGHT) and self.direction is not LEFT:
            self.direction = RIGHT

    def update_snake(self):
        """Move the snake by adding a head and optionally removing the tail."""
        old_head = self.snake[0]
        new_head = Point(old_head.x + self.direction.x,
                         old_head.y + self.direction.y)
        self.snake.appendleft(new_head)
        # Control speed by only popping the tail every 5 frames
        if pyxel.frame_count % 5 != 0:
            self.snake.pop()

    def check_death(self):
        """Check whether the snake has died (out-of-bounds or self-collision)."""
        head = self.snake[0]
        # Out of screen bounds (account for score area at top)
        if head.x < 0 or head.y <= HEIGHT_SCORE or \
           head.x >= WIDTH or head.y >= HEIGHT:
            self.death_event()
        # Ran into itself?
        elif len(self.snake) != len(set(self.snake)):
            self.death_event()

    def death_event(self):
        """Trigger game-over state."""
        self.death = True

    ##############
    # Draw logic #
    ##############

    def draw(self):
        """Draw the game or death screen depending on self.death."""
        if not self.death:
            pyxel.cls(col=COL_BACKGROUND)
            self.draw_snake()
        else:
            self.draw_death()

    def draw_snake(self):
        """Draw the snake with a distinct head color."""
        for i, point in enumerate(self.snake):
            col = COL_HEAD if i == 0 else COL_BODY
            pyxel.pset(point.x, point.y, col=col)

    def draw_death(self):
        """Draw a blank screen with centered death text."""
        pyxel.cls(col=COL_DEATH)
        for i, text in enumerate(TEXT_DEATH):
            y_offset = (pyxel.FONT_HEIGHT + 2) * i
            tx = self.center_text(text, WIDTH)
            pyxel.text(tx, HEIGHT_DEATH + y_offset, text, COL_TEXT_DEATH)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        """Calculate the X coordinate to center text on the screen."""
        text_width = len(text) * char_width
        return (page_width - text_width) // 2


# Start the game
Snake()