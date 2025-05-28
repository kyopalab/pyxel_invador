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

COL_BACKGROUND     = 3
COL_BODY           = 11
COL_HEAD           = 7
COL_DEATH          = 8
COL_APPLE          = 8

TEXT_DEATH         = ["GAME OVER", "(Q)UIT", "(R)ESTART"]
COL_TEXT_DEATH     = 0
HEIGHT_DEATH       = 5

WIDTH              = 40
HEIGHT             = 50

HEIGHT_SCORE       = pyxel.FONT_HEIGHT
COL_SCORE          = 6
COL_SCORE_BACKGROUND = 5

UP    = Point(0, -1)
DOWN  = Point(0, 1)
RIGHT = Point(1, 0)
LEFT  = Point(-1, 0)

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
        """Initiate key variables: direction, snake, score, death, apple."""
        self.direction    = RIGHT
        self.snake        = deque()
        self.snake.append(START)
        self.death        = False
        self.score        = 0                    # New: track apples eaten
        self.popped_point = None                 # For apple logic
        self.generate_apple()                    # Place first apple

    ##############
    # Game logic #
    ##############

    def update(self):
        """Update logic of game. Moves snake, checks apple/death, handles Q/R."""
        if not self.death:
            self.update_direction()
            self.update_snake()
            self.check_apple()   # New: handle eating
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
        """Move the snake by adding a new head and removing the tail."""
        old_head    = self.snake[0]
        new_head    = Point(old_head.x + self.direction.x,
                            old_head.y + self.direction.y)
        self.snake.appendleft(new_head)
        # Record the popped tail in case we need to restore it when eating
        self.popped_point = self.snake.pop()

    def check_apple(self):
        """Check whether the snake has eaten the apple."""
        # If new head is on the apple
        if self.snake[0] == self.apple:
            self.score += 1
            # Restore the tail so the snake grows by one
            self.snake.append(self.popped_point)
            self.generate_apple()

    def generate_apple(self):
        """Generate a new apple not on the snake."""
        snake_cells = set(self.snake)
        # Pick random until we find an empty cell
        while True:
            x = randint(0, WIDTH - 1)
            y = randint(HEIGHT_SCORE + 1, HEIGHT - 1)
            p = Point(x, y)
            if p not in snake_cells:
                self.apple = p
                break

    def check_death(self):
        """Check whether the snake has died (out-of-bounds or self-collision)."""
        head = self.snake[0]
        # Out of screen bounds (account for score area)
        if (head.x < 0 or head.y <= HEIGHT_SCORE or
            head.x >= WIDTH or head.y >= HEIGHT):
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
            self.draw_score()      # New: draw the current score
            self.draw_snake()
            # Draw the apple
            pyxel.pset(self.apple.x, self.apple.y, col=COL_APPLE)
        else:
            self.draw_death()

    def draw_snake(self):
        """Draw the snake with a distinct head color."""
        for i, point in enumerate(self.snake):
            col = COL_HEAD if i == 0 else COL_BODY
            pyxel.pset(point.x, point.y, col=col)

    def draw_score(self):
        """Draw the score at the top."""
        score_str = f"{self.score:04}"
        # Background bar
        pyxel.rect(0, 0, WIDTH, HEIGHT_SCORE, COL_SCORE_BACKGROUND)
        # Score text
        pyxel.text(1, 1, score_str, COL_SCORE)

    def draw_death(self):
        """Draw a blank screen with centered death text and final score."""
        pyxel.cls(col=COL_DEATH)
        # Insert the numeric score into the death messages
        display = TEXT_DEATH[:]
        display.insert(1, f" SCORE: {self.score:04} ")
        for i, txt in enumerate(display):
            y  = HEIGHT_DEATH + i * (pyxel.FONT_HEIGHT + 2)
            tx = self.center_text(txt, WIDTH)
            pyxel.text(tx, y, txt, COL_TEXT_DEATH)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        """Calculate the X coordinate to center text on the screen."""
        text_w = len(text) * char_width
        return (page_width - text_w) // 2


# Start the game
Snake()