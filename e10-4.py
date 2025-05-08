# -----------------------------------------------------------------------------
# File:    e10-4.py
# Project: FIT2 2025
# Author:  Kyopan
# Date:    2025-05-08
#
# Description:
#   Enhanced paddle game with bullets and colored balls.
#   Normal, bonus, and penalty balls affect scoring.
#   Press R to reset speed and shrink paddle; Z to fire bullets.
#   Levels add new balls every 10 catches; 10 misses ends the game.
#
# Usage:
#   pyxel run e10-4.py
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
import math

# Initialize a 200×200 window, 30 FPS, and enable mouse input
pyxel.init(200, 200, fps=30)
pyxel.mouse(True)

# --- Constants & State ---
initial_speed = 1.0
speed = initial_speed
score = 0
misses = 0
game_over = False
next_level_up_score = 10

# Paddle
pad_width = 40
pad_height = 5
pad_y = pyxel.height - 10
pad_x = (pyxel.width - pad_width) // 2

# Bullets
bullet_speed = 5
bullet_xs = []
bullet_ys = []

# Balls
ballxs = []
ballys = []
vxs = []
vys = []
ball_types = []  # 0=normal, 1=bonus, 2=penalty

def reset_ball(i):
    """Spawn ball i at top with random angle & type."""
    ballxs[i] = pyxel.rndi(0, pyxel.width - 1)
    ballys[i] = 0
    angle = pyxel.rndi(30, 150)
    vxs[i] = pyxel.cos(angle)
    vys[i] = pyxel.sin(angle)
    # assign type: 70% normal, 15% bonus, 15% penalty
    r = pyxel.rndi(1, 100)
    ball_types[i] = 1 if r <= 15 else 2 if r >= 86 else 0

# Start with one ball
for _ in range(1):
    ballxs.append(0); ballys.append(0)
    vxs.append(0); vys.append(0)
    ball_types.append(0)
    reset_ball(len(ballxs)-1)

def update():
    global pad_x, speed, score, misses, game_over, next_level_up_score, pad_width

    if game_over:
        return

    # -- Paddle follows mouse --
    pad_x = pyxel.mouse_x - pad_width // 2
    pad_x = max(0, min(pad_x, pyxel.width - pad_width))

    # -- Reset speed & shrink pad on key R --
    if pyxel.btnp(pyxel.KEY_R):
        speed = initial_speed
        pad_width = max(20, pad_width - 10)

    # -- Fire bullet on Z --
    if pyxel.btnp(pyxel.KEY_Z):
        bullet_xs.append(pad_x + pad_width//2)
        bullet_ys.append(pad_y)

    # -- Update bullets --
    for bi in reversed(range(len(bullet_xs))):
        bullet_ys[bi] -= bullet_speed
        if bullet_ys[bi] < 0:
            bullet_xs.pop(bi); bullet_ys.pop(bi)

    # -- Update balls --
    for i in range(len(ballxs)):
        ballxs[i] += vxs[i] * speed
        ballys[i] += vys[i] * speed

        # bounce walls
        if ballxs[i] <= 0 or ballxs[i] >= pyxel.width:
            vxs[i] = -vxs[i]

        # hit by bullet?
        for bi in reversed(range(len(bullet_xs))):
            dx = bullet_xs[bi] - ballxs[i]
            dy = bullet_ys[bi] - ballys[i]
            if dx*dx + dy*dy < 10*10:
                # destroy ball
                reset_ball(i)
                bullet_xs.pop(bi); bullet_ys.pop(bi)
                score += 1  # give 1 point for shooting
                break

        # reached bottom?
        if ballys[i] >= pyxel.height:
            # caught by paddle?
            if pad_x <= ballxs[i] <= pad_x + pad_width:
                # normal / bonus / penalty logic
                if ball_types[i] == 1:
                    score += 3
                elif ball_types[i] == 2:
                    score = max(0, score - 1)
                else:
                    score += 1
                # level up?
                if score >= next_level_up_score:
                    # add a new ball
                    ballxs.append(0); ballys.append(0)
                    vxs.append(0); vys.append(0)
                    ball_types.append(0)
                    reset_ball(len(ballxs)-1)
                    speed = initial_speed
                    pad_width = 40  # reset paddle size
                    next_level_up_score += 10
            else:
                misses += 1
                if misses >= 10:
                    game_over = True

            speed += 0.1
            reset_ball(i)

def draw():
    # -- Game Over Overlay --
    if game_over:
        pyxel.text(70, 90, "GAME OVER", 8)
        pyxel.text(60, 110, f"Final Score: {score}", 7)
        return

    # -- Clear & Draw --
    pyxel.cls(7)

    # draw bullets
    for x, y in zip(bullet_xs, bullet_ys):
        pyxel.rect(x-1, y, 2, 6, 12)

    # draw balls
    for x, y, t in zip(ballxs, ballys, ball_types):
        color = 6 if t == 0 else 10 if t == 1 else 8
        pyxel.circ(x, y, 10, color)

    # draw paddle
    pyxel.rect(pad_x, pad_y, pad_width, pad_height, 11)

    # HUD
    pyxel.text(5, 5, f"Score: {score}", 0)
    pyxel.text(5, 15, f"Misses: {misses}", 0)
    pyxel.text(5, 25, "R: slow+shrink pad", 0)
    pyxel.text(5, 35, "Z: shoot bullet", 0)

pyxel.run(update, draw)