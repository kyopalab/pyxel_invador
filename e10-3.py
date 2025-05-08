# -----------------------------------------------------------------------------
# File:    e10-3.py
# Project: FIT2 2025
# Author:  Kyopan
# Date:    2025-05-08
#
# Description:
#   Mouse-controlled paddle game where balls increase each level.
#   Every 10 catches adds a new ball and resets speed; 10 misses ends the game.
#
# Usage:
#   pyxel run e10-3.py
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
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
# -----------------------------------------------------------------------------
import pyxel

# Initialize a 200×200 window, 30 FPS, and enable mouse input
pyxel.init(200, 200, fps=30)
pyxel.mouse(True)

# Game parameters
initial_speed = 1.0          # base speed to reset to on level up
speed = initial_speed        # current speed multiplier
score = 0                    # number of successful catches
misses = 0                   # number of misses
game_over = False            # flag for end of game
next_level_up_score = 10     # score threshold for adding a new ball

# Paddle dimensions and position
pad_width = 40
pad_height = 5
pad_y = pyxel.height - 10    # 10 px above bottom
pad_x = (pyxel.width - pad_width) // 2

# Ball state stored in lists so we can handle a variable number of balls
ballxs = []
ballys = []
vxs = []
vys = []

def reset_ball(i):
    """Initialize ball i at a random x along the top with a random launch angle."""
    ballxs[i] = pyxel.rndi(0, pyxel.width - 1)
    ballys[i] = 0
    angle = pyxel.rndi(30, 150)
    vxs[i] = pyxel.cos(angle)
    vys[i] = pyxel.sin(angle)

# Spawn the very first ball
ballxs.append(0)
ballys.append(0)
vxs.append(0)
vys.append(0)
reset_ball(0)

def update():
    global pad_x, speed, score, misses, game_over, next_level_up_score

    # If the game has ended, skip all updates
    if game_over:
        return

    # Paddle follows the mouse’s X coordinate
    pad_x = pyxel.mouse_x - pad_width // 2
    pad_x = max(0, min(pad_x, pyxel.width - pad_width))

    # Update each ball
    for i in range(len(ballxs)):
        # Move ball by its velocity scaled by speed
        ballxs[i] += vxs[i] * speed
        ballys[i] += vys[i] * speed

        # Bounce off the left and right walls
        if ballxs[i] <= 0 or ballxs[i] >= pyxel.width:
            vxs[i] = -vxs[i]

        # If the ball reaches the bottom…
        if ballys[i] >= pyxel.height:
            # Check if the paddle caught it
            if pad_x <= ballxs[i] <= pad_x + pad_width:
                score += 1
                # Level up every 10 catches
                if score >= next_level_up_score:
                    # Add a new ball
                    ballxs.append(0)
                    ballys.append(0)
                    vxs.append(0)
                    vys.append(0)
                    reset_ball(len(ballxs) - 1)
                    # Reset speed to the original slow speed
                    speed = initial_speed
                    # Schedule the next level-up threshold
                    next_level_up_score += 10
            else:
                misses += 1
                # End the game after 10 misses
                if misses >= 10:
                    game_over = True
            # Speed up for the next launch of this ball
            speed += 0.1
            # Reset this ball for its next launch
            reset_ball(i)

def draw():
    # If game over, display a message and final score without clearing the screen
    if game_over:
        pyxel.text(80, 90, "GAME OVER", 8)
        pyxel.text(70, 110, f"Final Score: {score}", 7)
        return

    # Otherwise, draw the current game state
    pyxel.cls(7)  # clear background

    # Draw all balls
    for i in range(len(ballxs)):
        pyxel.circ(ballxs[i], ballys[i], 10, 6)

    # Draw the paddle
    pyxel.rect(pad_x, pad_y, pad_width, pad_height, 11)

    # Draw the score and miss count
    pyxel.text(5, 5, f"Score: {score}", 0)
    pyxel.text(5, 15, f"Misses: {misses}", 0)

# Start the game loop
pyxel.run(update, draw)