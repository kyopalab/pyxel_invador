# -----------------------------------------------------------------------------
# File:    e11-1_ex.py
# Project: FIT2 2025
# Author:  Kyopan
# Date:    2025-05-21
#
# Description:
#   Enhanced paddle game with bullets and colored balls.
#   Normal, bonus, and penalty balls affect scoring.
#   Press R to reset speed and shrink paddle; Z to fire bullets.
#   Levels add new balls every 10 catches; 10 misses ends the game.
#
# Usage:
#   pyxel run e11-1_ex.py
#
# Controls:
#   - Mouse: Move paddle horizontally
#   - Z key: Shoot bullets
#   - R key: Reset speed & shrink paddle
#
# Dependencies:
#   - pyxel (https://github.com/kitao/pyxel)
#
# License:
#   MIT License
# -----------------------------------------------------------------------------

import pyxel
import math

# Initialize a 200×200 window, 30 FPS, and enable mouse input
pyxel.init(200, 200, fps=30)
pyxel.mouse(True)

# --- Constants & State ---
initial_speed        = 1.0
speed                = initial_speed
score                = 0
misses               = 0
game_over            = False
next_level_up_score  = 10

# Paddle
pad_width = 40
pad_height = 5
pad_y      = pyxel.height - 10
pad_x      = (pyxel.width - pad_width) // 2

# Bullets
bullet_speed = 5
bullet_xs    = []
bullet_ys    = []

class Ball:
    """A ball with its own position, velocity, and type."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Set initial position at top and random angle & type."""
        self.x = pyxel.rndi(0, pyxel.width - 1)
        self.y = 0
        angle  = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)
        r = pyxel.rndi(1, 100)
        self.type = 1 if r <= 15 else 2 if r >= 86 else 0  # bonus/penalty/normal

    def update(self, speed):
        """
        Move the ball, bounce off walls, and return True if it reached bottom.
        """
        # Move
        self.x += self.vx * speed
        self.y += self.vy * speed

        # Bounce off left/right edges
        if self.x <= 0 or self.x >= pyxel.width:
            self.vx = -self.vx

        # Check bottom
        return self.y >= pyxel.height

    def draw(self):
        """Draw the ball in color based on its type."""
        color = 6 if self.type == 0 else 10 if self.type == 1 else 8
        pyxel.circ(self.x, self.y, 10, color)


# Initialize first ball
balls = [Ball()]

def update():
    global pad_x, speed, score, misses, game_over, next_level_up_score, pad_width

    if game_over:
        return

    # Paddle follows mouse
    pad_x = pyxel.mouse_x - pad_width // 2
    pad_x = max(0, min(pad_x, pyxel.width - pad_width))

    # Reset speed & shrink pad on R
    if pyxel.btnp(pyxel.KEY_R):
        speed = initial_speed
        pad_width = max(20, pad_width - 10)

    # Fire bullet on Z
    if pyxel.btnp(pyxel.KEY_Z):
        bullet_xs.append(pad_x + pad_width // 2)
        bullet_ys.append(pad_y)

    # Update bullets
    for bi in reversed(range(len(bullet_xs))):
        bullet_ys[bi] -= bullet_speed
        if bullet_ys[bi] < 0:
            bullet_xs.pop(bi)
            bullet_ys.pop(bi)

    # Update balls
    for ball in balls:
        hit_bottom = ball.update(speed)

        # Check bullet collisions
        for bi in reversed(range(len(bullet_xs))):
            dx = bullet_xs[bi] - ball.x
            dy = bullet_ys[bi] - ball.y
            if dx*dx + dy*dy < 100:  # within radius 10
                ball.reset()
                bullet_xs.pop(bi)
                bullet_ys.pop(bi)
                score += 1
                break

        # Handle bottom
        if hit_bottom:
            # Caught by paddle?
            if pad_x <= ball.x <= pad_x + pad_width:
                # Apply scoring based on type
                if ball.type == 1:
                    score += 3
                elif ball.type == 2:
                    score = max(0, score - 1)
                else:
                    score += 1
                # Level up
                if score >= next_level_up_score:
                    balls.append(Ball())
                    speed = initial_speed
                    pad_width = 40
                    next_level_up_score += 10
            else:
                misses += 1
                if misses >= 10:
                    game_over = True
            # Speed up and reset ball
            speed += 0.1
            ball.reset()

def draw():
    # Game Over overlay
    if game_over:
        pyxel.text(70, 90, "GAME OVER", 8)
        pyxel.text(60, 110, f"Final Score: {score}", 7)
        return

    # Clear & draw
    pyxel.cls(7)

    # Draw bullets
    for x, y in zip(bullet_xs, bullet_ys):
        pyxel.rect(x-1, y, 2, 6, 12)

    # Draw balls
    for ball in balls:
        ball.draw()

    # Draw paddle
    pyxel.rect(pad_x, pad_y, pad_width, pad_height, 11)

    # HUD
    pyxel.text(5, 5, f"Score: {score}", 0)
    pyxel.text(5, 15, f"Misses: {misses}", 0)
    pyxel.text(5, 25, "R: slow+shrink pad", 0)
    pyxel.text(5, 35, "Z: shoot bullet", 0)

pyxel.run(update, draw)