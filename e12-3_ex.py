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
        """Initialize at random top X, zero Y, random angle & type."""
        self.x = pyxel.rndi(0, pyxel.width - 1)
        self.y = 0
        angle  = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)
        r       = pyxel.rndi(1, 100)
        # 0 = normal, 1 = bonus, 2 = penalty
        self.type = 1 if r <= 15 else 2 if r >= 86 else 0

    def move(self, speed):
        """
        Move the ball; bounce off left/right edges.
        If it reaches bottom, restart and return True.
        """
        self.x += self.vx * speed
        self.y += self.vy * speed

        # bounce horizontally
        if self.x <= 0 or self.x >= pyxel.width:
            self.vx = -self.vx

        # bottom check
        if self.y >= pyxel.height:
            self.restart()
            return True

        return False

    def update(self, speed):
        """Advance the ball and report bottom collision."""
        return self.move(speed)

    def draw(self):
        """Draw the ball based on its type."""
        color = 6 if self.type == 0 else 10 if self.type == 1 else 8
        pyxel.circ(self.x, self.y, 10, color)


class Pad:
    """Mouse-controlled paddle with catch logic."""
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
        Handle a ball that has reached the bottom:
        update score/misses, manage level-ups, and end the game if needed.
        """
        global score, misses, speed, next_level_up_score, game_over

        if self.x <= ball.x <= self.x + self.width:
            # caught
            if ball.type == 1:
                score += 3
            elif ball.type == 2:
                score = max(0, score - 1)
            else:
                score += 1

            if score >= next_level_up_score:
                balls.append(Ball())
                speed = initial_speed
                self.width = 40
                next_level_up_score += 10
        else:
            # missed
            misses += 1
            if misses >= 10:
                game_over = True


# Instantiate game objects
pad   = Pad()
balls = [Ball()]

def update():
    global speed

    if game_over:
        return

    # Update paddle
    pad.update()

    # R: reset speed & shrink paddle
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

    # Update balls and handle bottom collisions
    for ball in balls:
        hit_bottom = ball.update(speed)

        # Bullet collision
        for bi in reversed(range(len(bullet_xs))):
            dx = bullet_xs[bi] - ball.x
            dy = bullet_ys[bi] - ball.y
            if dx*dx + dy*dy < 100:
                ball.restart()
                bullet_xs.pop(bi)
                bullet_ys.pop(bi)
                score += 1
                break

        # Bottom event: delegate to pad.catch()
        if hit_bottom:
            pad.catch(ball)
            speed += 0.1

def draw():
    if game_over:
        pyxel.cls(7)
        pyxel.text(70,  90, "GAME OVER",        8)
        pyxel.text(60, 110, f"Final Score: {score}", 7)
        return

    pyxel.cls(7)

    # Draw bullets
    for x, y in zip(bullet_xs, bullet_ys):
        pyxel.rect(x - 1, y, 2, 6, 12)

    # Draw balls
    for ball in balls:
        ball.draw()

    # Draw paddle
    pad.draw()

    # HUD
    pyxel.text(5,  5, f"Score:   {score}", 0)
    pyxel.text(5, 15, f"Misses: {misses}", 0)
    pyxel.text(5, 25, "R: slow+shrink pad", 0)
    pyxel.text(5, 35, "Z: shoot bullet",   0)

# Start the game
pyxel.run(update, draw)