# -----------------------------------------------------------------------------
# File:    e11-1.py
# Project: FIT2 2025
# Author:  Kyopan
# Date:    2025-05-16
#
# Description:
#   Class-based implementation of a mouse-controlled paddle game based on e10-3.py.  
#   Mouse-controlled paddle game where balls increase each level.
#   Every 10 catches adds a new ball and resets speed; 10 misses ends the game. 
#
# Usage:
#   pyxel run e11-1.py
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
#
#   Copyright (c) 2025 Kyopan
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

# Paddle dimensions and position
pad_width = 40
pad_height = 5
pad_y = pyxel.height - 10
pad_x = (pyxel.width - pad_width) // 2

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

    def update(self, speed):
        """Move the ball; bounce off sides. Return True if reached bottom."""
        self.x += self.vx * speed
        self.y += self.vy * speed
        # bounce off left/right walls
        if self.x <= 0 or self.x >= pyxel.width:
            self.vx = -self.vx
        # if reached bottom edge, indicate reset needed
        if self.y >= pyxel.height:
            return True
        return False

    def draw(self):
        """Render the ball as a circle."""
        pyxel.circ(self.x, self.y, 10, 6)

# Initialize first ball
balls = [Ball()]

def update():
    global pad_x, speed, score, misses, game_over, next_level_up_score

    # If game has ended, skip update
    if game_over:
        return

    # Move paddle with mouse
    pad_x = pyxel.mouse_x - pad_width // 2
    pad_x = max(0, min(pad_x, pyxel.width - pad_width))

    # Update each ball instance
    for ball in balls:
        reached_bottom = ball.update(speed)
        if reached_bottom:
            # caught?
            if pad_x <= ball.x <= pad_x + pad_width:
                score += 1
                # level up when threshold reached
                if score >= next_level_up_score:
                    balls.append(Ball())
                    speed = initial_speed
                    next_level_up_score += 10
            else:
                misses += 1
                if misses >= 10:
                    game_over = True
            speed += 0.1
            ball.reset()

def draw():
    # If game over, overlay message
    if game_over:
        pyxel.cls(7)
        pyxel.text(80, 90, "GAME OVER", 8)
        pyxel.text(70, 110, f"Final Score: {score}", 7)
        return

    # Draw playing field
    pyxel.cls(7)
    for ball in balls:
        ball.draw()

    # Draw paddle
    pyxel.rect(pad_x, pad_y, pad_width, pad_height, 11)

    # Draw HUD
    pyxel.text(5, 5, f"Score: {score}", 0)
    pyxel.text(5, 15, f"Misses: {misses}", 0)

# Start game loop
pyxel.run(update, draw)