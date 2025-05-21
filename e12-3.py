# -----------------------------------------------------------------------------
# File:    e12-3.py
# Project: FIT2 2025
# Author:  Kyopan
# Date:    2025-05-20
#
# Description:
#   Mouse-controlled paddle game where balls increase each level.
#   Every 10 catches adds a new ball and resets speed; 10 misses ends the game.
#
# Usage:
#   pyxel run e12-3.py
#
# Controls:
#   - Mouse: Move paddle horizontally
#   - Catch balls to earn points; 10 misses ends the game
#
# Dependencies:
#   - pyxel (https://github.com/kitao/pyxel)
#
# License:
#   MIT License
# -----------------------------------------------------------------------------

import pyxel

# Initialize a 200×200 window, 30 FPS, and enable mouse input
pyxel.init(200, 200, fps=30)
pyxel.mouse(True)

# Game parameters
initial_speed = 1.0          # base speed to reset on level up
speed = initial_speed        # current speed multiplier
score = 0                    # caught ball count
misses = 0                   # missed ball count
game_over = False            # end flag
next_level_up_score = 10     # threshold to add new ball

class Ball:
    """A single falling ball with its own position and velocity."""
    def __init__(self):
        self.restart()

    def restart(self):
        """Initialize position at random top X, and random launch angle."""
        self.x  = pyxel.rndi(0, pyxel.width - 1)
        self.y  = 0
        angle   = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)

    def move(self, speed):
        """
        Move the ball and bounce off left/right edges.
        If it reaches bottom, restart and return True.
        """
        self.x += self.vx * speed
        self.y += self.vy * speed

        # Horizontal bounce
        if self.x <= 0 or self.x >= pyxel.width:
            self.vx = -self.vx

        # If hit bottom edge, restart and signal
        if self.y >= pyxel.height:
            self.restart()
            return True
        return False

    def update(self, speed):
        """Advance the ball and indicate bottom-collision via move()."""
        return self.move(speed)

    def draw(self):
        """Render the ball as a circle."""
        pyxel.circ(self.x, self.y, 10, 6)


class Pad:
    """Mouse-controlled paddle with its own catch logic."""
    def __init__(self):
        self.width  = 40
        self.height = 5
        self.y      = pyxel.height - 10
        self.x      = (pyxel.width - self.width) // 2

    def update(self):
        """Follow the mouse's x-position, clamped to screen bounds."""
        self.x = pyxel.mouse_x - self.width // 2
        self.x = max(0, min(self.x, pyxel.width - self.width))

    def draw(self):
        """Render the paddle as a rectangle."""
        pyxel.rect(self.x, self.y, self.width, self.height, 11)

    def catch(self, ball):
        """
        Called when a ball reaches the bottom.
        Updates score/misses, handles level-up, and game over.
        """
        global score, misses, speed, next_level_up_score, game_over

        # If the ball's X is within paddle bounds → caught
        if self.x <= ball.x <= self.x + self.width:
            score += 1
            # Level up: add a new ball every threshold
            if score >= next_level_up_score:
                balls.append(Ball())
                speed = initial_speed
                next_level_up_score += 10
        else:
            # Missed
            misses += 1
            if misses >= 10:
                game_over = True

# Initialize game objects
balls = [Ball()]
pad   = Pad()

def update():
    global speed

    if game_over:
        return

    # Update paddle
    pad.update()

    # Update each ball; if bottom collision, delegate catch logic
    for ball in balls:
        if ball.update(speed):
            pad.catch(ball)
            speed += 0.1

def draw():
    # If game over, show overlay
    if game_over:
        pyxel.cls(7)
        pyxel.text(80, 90, "GAME OVER", 8)
        pyxel.text(70, 110, f"Final Score: {score}", 7)
        return

    # Draw playfield
    pyxel.cls(7)
    for ball in balls:
        ball.draw()
    pad.draw()

    # Draw HUD
    pyxel.text(5,  5, f"Score:   {score}",  0)
    pyxel.text(5, 15, f"Misses: {misses}", 0)

# Start the game loop
pyxel.run(update, draw)