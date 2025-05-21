# -----------------------------------------------------------------------------
# File:    e12-1.py
# Project: FIT2 2025
# Author:  Kyopan
# Date:    2025-05-08
#
# Description:
#   Mouse-controlled paddle game where balls increase each level.
#   Every 10 catches adds a new ball and resets speed; 10 misses ends the game.
#
# Usage:
#   pyxel run e12-1.py
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
        self.reset()

    def reset(self):
        """Position at random X along top, random angle between 30°–150°."""
        self.x = pyxel.rndi(0, pyxel.width - 1)
        self.y = 0
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)

    def move(self, speed):
        """Move the ball and bounce off the left/right edges."""
        self.x += self.vx * speed
        self.y += self.vy * speed
        if self.x <= 0 or self.x >= pyxel.width:
            self.vx = -self.vx

    def update(self, speed):
        """Advance the ball; return True if it reached the bottom."""
        self.move(speed)
        return self.y >= pyxel.height

    def draw(self):
        """Render the ball as a circle."""
        pyxel.circ(self.x, self.y, 10, 6)

class Pad:
    """Mouse-controlled paddle."""
    def __init__(self):
        self.width  = 40
        self.height = 5
        self.y      = pyxel.height - 10
        self.x      = (pyxel.width - self.width) // 2

    def update(self):
        """Follow the mouse's x-position, clamped to the screen."""
        self.x = pyxel.mouse_x - self.width // 2
        self.x = max(0, min(self.x, pyxel.width - self.width))

    def draw(self):
        """Render the paddle as a rectangle."""
        pyxel.rect(self.x, self.y, self.width, self.height, 11)

# Initialize first ball and pad
balls = [Ball()]
pad   = Pad()

def update():
    global speed, score, misses, game_over, next_level_up_score

    # If the game has ended, skip updates
    if game_over:
        return

    # Update paddle position
    pad.update()

    # Update each ball
    for ball in balls:
        if ball.update(speed):
            # Ball reached bottom: check catch
            if pad.x <= ball.x <= pad.x + pad.width:
                score += 1
                # Level up: add a new ball when threshold reached
                if score >= next_level_up_score:
                    balls.append(Ball())
                    speed = initial_speed
                    next_level_up_score += 10
            else:
                misses += 1
                if misses >= 10:
                    game_over = True
            # Speed up next launch and reset the ball
            speed += 0.1
            ball.reset()

def draw():
    # If game over, display overlay message
    if game_over:
        pyxel.cls(7)
        pyxel.text(80, 90, "GAME OVER", 8)
        pyxel.text(70, 110, f"Final Score: {score}", 7)
        return

    # Draw game field
    pyxel.cls(7)
    for ball in balls:
        ball.draw()
    pad.draw()

    # Draw HUD
    pyxel.text(5,  5, f"Score:   {score}",  0)
    pyxel.text(5, 15, f"Misses: {misses}", 0)

# Start the game loop
pyxel.run(update, draw)