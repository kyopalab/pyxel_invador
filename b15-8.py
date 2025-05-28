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

COL_BACKGROUND       = 3
COL_BODY             = 11
COL_HEAD             = 7
COL_DEATH            = 8
COL_APPLE            = 8

TEXT_DEATH           = ["GAME OVER", "(Q)UIT", "(R)ESTART"]
COL_TEXT_DEATH       = 0
HEIGHT_DEATH         = 5

WIDTH                = 40
HEIGHT               = 50

HEIGHT_SCORE         = pyxel.FONT_HEIGHT
COL_SCORE            = 6
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
        """Initiate pyxel, set up sounds, game variables, and run."""
        pyxel.init(WIDTH, HEIGHT, fps=2)
        define_sound_and_music()          # Load SFX and music tables
        self.reset()
        pyxel.playm(0, loop=True)         # Start background music track 0
        pyxel.run(self.update, self.draw)

    def reset(self):
        """Initiate key variables: direction, snake, score, death, apple."""
        self.direction    = RIGHT
        self.snake        = deque([START])
        self.death        = False
        self.score        = 0                    # track apples eaten
        self.popped_point = None                 # for apple logic
        self.generate_apple()                    # place first apple
        pyxel.playm(0, loop=True)                # ensure music restarts

    ##############
    # Game logic #
    ##############

    def update(self):
        """Update logic of game. Moves snake, checks apple/death, handles Q/R."""
        if not self.death:
            self.update_direction()
            self.update_snake()
            self.check_apple()   # play eat sound
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
        old_head = self.snake[0]
        new_head = Point(old_head.x + self.direction.x,
                         old_head.y + self.direction.y)
        self.snake.appendleft(new_head)
        self.popped_point = self.snake.pop()      # record tail for apple growth

    def check_apple(self):
        """Check whether the snake has eaten the apple."""
        if self.snake[0] == self.apple:
            self.score += 1
            self.snake.append(self.popped_point)  # grow by restoring tail
            pyxel.play(0, 0)                      # play eat SFX
            self.generate_apple()

    def generate_apple(self):
        """Generate a new apple not on the snake."""
        snake_cells = set(self.snake)
        while True:
            x = randint(0, WIDTH - 1)
            y = randint(HEIGHT_SCORE + 1, HEIGHT - 1)
            p = Point(x, y)
            if p not in snake_cells:
                self.apple = p
                return

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
        """Trigger game-over state and play death SFX/music."""
        self.death = True
        pyxel.stop()           # stop all sounds/music
        pyxel.play(0, 1)       # play track 1 as death jingle

    ##############
    # Draw logic #
    ##############

    def draw(self):
        """Draw the game or death screen depending on self.death."""
        if not self.death:
            pyxel.cls(col=COL_BACKGROUND)
            self.draw_score()
            self.draw_snake()
            pyxel.pset(self.apple.x, self.apple.y, col=COL_APPLE)
        else:
            self.draw_death()

    def draw_snake(self):
        """Draw the snake with a distinct head color."""
        for i, pt in enumerate(self.snake):
            col = COL_HEAD if i == 0 else COL_BODY
            pyxel.pset(pt.x, pt.y, col=col)

    def draw_score(self):
        """Draw the score at the top."""
        s = f"{self.score:04}"
        pyxel.rect(0, 0, WIDTH, HEIGHT_SCORE, COL_SCORE_BACKGROUND)
        pyxel.text(1, 1, s, COL_SCORE)

    def draw_death(self):
        """Draw a blank screen with centered death text and final score."""
        pyxel.cls(col=COL_DEATH)
        msgs = TEXT_DEATH[:]
        msgs.insert(1, f"SCORE: {self.score:04}")
        for i, txt in enumerate(msgs):
            y = HEIGHT_DEATH + i * (pyxel.FONT_HEIGHT + 2)
            x = self.center_text(txt, WIDTH)
            pyxel.text(x, y, txt, COL_TEXT_DEATH)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        """Calculate the X coordinate to center text on the screen."""
        tw = len(text) * char_width
        return (page_width - tw) // 2


###########################
# Music and sound effects #
###########################

def define_sound_and_music():
    """Define sound and music."""
    # Sound effects
    pyxel.sounds[0].set(
        notes="c3e3g3c4c4",
        tones="s",
        volumes="4",
        effects=("n"*4 + "f"),
        speed=7,
    )
    pyxel.sounds[1].set(
        notes="f3 b2 f2 b1  f1 f1 f1 f1",
        tones="p",
        volumes=("4"*4 + "4321"),
        effects=("n"*7 + "f"),
        speed=9,
    )

    melody1 = (
        "c3 c3 c3 d3 e3 r e3 r"
        + ("r"*8)
        + "e3 e3 e3 f3 d3 r c3 r"
        + ("r"*8)
        + "c3 c3 c3 d3 e3 r e3 r"
        + ("r"*8)
        + "b2 b2 b2 f3 d3 r c3 r"
        + ("r"*8)
    )
    melody2 = (
        "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 g2g2g2g2 c3c3c3c3 g2g2a2a2"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "f3f3f3a3 a3a3a3a3 g3g3g3b3 b3b3b3b3"
        + "b3b3b3b4 rrrr e3d3c3g3 a2g2e2d2"
    )
    # Music tracks
    pyxel.sounds[2].set(
        notes=melody1*2 + melody2*2,
        tones="s",
        volumes="3",
        effects="nnnsffff",
        speed=20,
    )
    harmony1 = ("a1 a1 a1 b1  f1 f1 c2 c2" "c2"*3)*1 + "f1"*16
    harmony2 = ("f1"*8 + "g1"*8 + "a1"*8 + "c2"*7 + "d2")*3 + "f1"*16 + "g1"*16
    pyxel.sounds[3].set(
        notes=harmony1*2 + harmony2*2,
        tones="t",
        volumes="5",
        effects="f",
        speed=20,
    )
    pyxel.sounds[4].set(
        notes="f0 r a4 r  f0 f0 a4 r f0 r a4 r   f0 f0 a4 f0",
        tones="n",
        volumes="6622 6622 6622 6426",
        effects="f",
        speed=20,
    )
    pyxel.music(0).set([], [2], [3], [4])


# Start the game
Snake()