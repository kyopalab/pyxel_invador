# -----------------------------------------------------------------------------
# File:    e12-2_ex.py
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
#   pyxel run e12-2_ex.py
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

# Initialize a 200×200 window, 30 FPS, and enable mouse input
pyxel.init(200, 200, fps=30)
pyxel.mouse(True)

# --- Game State ---
initial_speed       = 1.0
speed               = initial_speed
score               = 0
misses              = 0
game_over           = False
next_level_up_score = 10

# Bullet state
bullet_speed = 5
bullet_xs    = []
bullet_ys    = []

class Ball:
    """A ball with its own position, velocity, and type."""
    def __init__(self):
        self.restart()

    def restart(self):
        """Place at random top-X, zero Y, random 30°–150° angle & type."""
        self.x = pyxel.rndi(0, pyxel.width - 1)
        self.y = 0
        angle  = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)
        # 70% normal, 15% bonus, 15% penalty
        r = pyxel.rndi(1, 100)
        self.type = 1 if r <= 15 else 2 if r >= 86 else 0

    def move(self, speed):
        """
        Move the ball, bounce off sides, and if it reaches bottom:
        restart() and return True; else return False.
        """
        # advance
        self.x += self.vx * speed
        self.y += self.vy * speed

        # bounce off left/right
        if self.x <= 0 or self.x >= pyxel.width:
            self.vx = -self.vx

        # bottom check
        if self.y >= pyxel.height:
            self.restart()
            return True

        return False

    def update(self, speed):
        """Wrapper that returns whether bottom was hit."""
        return self.move(speed)

    def draw(self):
        """Draw in color by type."""
        color = 6 if self.type == 0 else 10 if self.type == 1 else 8
        pyxel.circ(self.x, self.y, 10, color)


class Pad:
    """Mouse-controlled paddle."""
    def __init__(self):
        self.width  = 40
        self.height = 5
        self.y      = pyxel.height - 10
        self.x      = (pyxel.width - self.width) // 2

    def update(self):
        """Follow mouse X, clamped in bounds."""
        self.x = pyxel.mouse_x - self.width // 2
        self.x = max(0, min(self.x, pyxel.width - self.width))

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 11)


# Instantiate game objects
pad   = Pad()
balls = [Ball()]

def update():
    global speed, score, misses, game_over, next_level_up_score, pad, bullet_xs, bullet_ys

    if game_over:
        return

    # Move paddle
    pad.update()

    # R: reset speed & shrink pad
    if pyxel.btnp(pyxel.KEY_R):
        speed = initial_speed
        pad.width = max(20, pad.width - 10)

    # Z: fire bullet
    if pyxel.btnp(pyxel.KEY_Z):
        bullet_xs.append(pad.x + pad.width // 2)
        bullet_ys.append(pad.y)

    # Update bullets
    for bi in reversed(range(len(bullet_xs))):
        bullet_ys[bi] -= bullet_speed
        if bullet_ys[bi] < 0:
            bullet_xs.pop(bi)
            bullet_ys.pop(bi)

    # Update balls
    for ball in balls:
        hit_bottom = ball.update(speed)

        # bullet collision
        for bi in reversed(range(len(bullet_xs))):
            dx = bullet_xs[bi] - ball.x
            dy = bullet_ys[bi] - ball.y
            if dx*dx + dy*dy < 100:
                ball.restart()
                bullet_xs.pop(bi)
                bullet_ys.pop(bi)
                score += 1
                break

        # bottom event
        if hit_bottom:
            # catch?
            if pad.x <= ball.x <= pad.x + pad.width:
                # scoring by type
                if ball.type == 1:
                    score += 3
                elif ball.type == 2:
                    score = max(0, score - 1)
                else:
                    score += 1
                # level-up
                if score >= next_level_up_score:
                    balls.append(Ball())
                    speed = initial_speed
                    pad.width = 40
                    next_level_up_score += 10
            else:
                misses += 1
                if misses >= 10:
                    game_over = True

            # speed up for next launch
            speed += 0.1

def draw():
    if game_over:
        pyxel.cls(7)
        pyxel.text(70,  90, "GAME OVER",    8)
        pyxel.text(60, 110, f"Final Score: {score}", 7)
        return

    pyxel.cls(7)

    # draw bullets
    for x, y in zip(bullet_xs, bullet_ys):
        pyxel.rect(x-1, y, 2, 6, 12)

    # draw balls
    for ball in balls:
        ball.draw()

    # draw paddle
    pad.draw()

    # HUD
    pyxel.text(5,  5, f"Score:   {score}",  0)
    pyxel.text(5, 15, f"Misses: {misses}", 0)
    pyxel.text(5, 25, "R: slow+shrink pad", 0)
    pyxel.text(5, 35, "Z: shoot bullet",   0)

# Start the game
pyxel.run(update, draw)