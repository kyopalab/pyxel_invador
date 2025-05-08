# -----------------------------------------------------------------------------
# File:    e10-1.py
# Project: FIT2 2025
# Author:  Kyopan
# Date:    2025-05-08
#
# Description:
#   A mouse-controlled paddle game where multiple balls fall from the top
#   at random angles. You catch balls to earn points, and the speed
#   increases with each catch.
#
# Usage:
#   pyxel run e10-1.py
#
# Controls:
#   - Mouse: Move the paddle horizontally
#   - Catch falling balls to increase score
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

# Initialize a 200×200 window
pyxel.init(200, 200)
pyxel.mouse(True)

# Game parameters
ball_count = 3
speed = 1.0
score = 0

# Paddle dimensions
pad_width = 40
pad_height = 5
pad_y = pyxel.height - 10  # 10 px above bottom
pad_x = (pyxel.width - pad_width) // 2

# Lists to hold each ball’s state
ballxs = [0] * ball_count
ballys = [0] * ball_count
vxs = [0] * ball_count
vys = [0] * ball_count

def reset_ball(i):
    """Place ball i at a random x along the top with a random angle 30°–150°."""
    ballxs[i] = pyxel.rndi(0, pyxel.width - 1)
    ballys[i] = 0
    angle = pyxel.rndi(30, 150)
    vxs[i] = pyxel.cos(angle)
    vys[i] = pyxel.sin(angle)

# Initialize all balls
for i in range(ball_count):
    reset_ball(i)

def update():
    global pad_x, speed, score

    # Paddle follows mouse X
    pad_x = pyxel.mouse_x - pad_width // 2
    pad_x = max(0, min(pad_x, pyxel.width - pad_width))

    # Update each ball
    for i in range(ball_count):
        ballxs[i] += vxs[i] * speed
        ballys[i] += vys[i] * speed

        # Bounce off left/right edges
        if ballxs[i] <= 0 or ballxs[i] >= pyxel.width:
            vxs[i] = -vxs[i]

        # When ball reaches bottom
        if ballys[i] >= pyxel.height:
            # Check catch
            if pad_x <= ballxs[i] <= pad_x + pad_width:
                score += 1
            # Speed up next round
            speed += 0.1
            # Reset this ball
            reset_ball(i)

def draw():
    # Clear screen
    pyxel.cls(7)
    # Draw balls
    for i in range(ball_count):
        pyxel.circ(ballxs[i], ballys[i], 10, 6)
    # Draw paddle
    pyxel.rect(pad_x, pad_y, pad_width, pad_height, 11)
    # Draw score
    pyxel.text(5, 5, f"Score: {score}", 0)

# Start the game loop
pyxel.run(update, draw)