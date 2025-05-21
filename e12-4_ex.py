# -----------------------------------------------------------------------------
# File:    e12-4_ex.py
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
#   pyxel run e12-4_ex.py
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

        if self.x <= 0 or self.x >= pyxel.width:
            self.vx = -self.vx

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
        """Follow mouse X; clamp within screen."""
        self.x = pyxel.mouse_x - self.width // 2
        self.x = max(0, min(self.x, pyxel.width - self.width))

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 11)

    def catch(self, ball, state):
        """
        Handle a ball that hit the bottom:
        update state.score, state.misses, add new balls, and set game_over.
        """
        if self.x <= ball.x <= self.x + self.width:
            # caught
            if ball.type == 1:
                state.score += 3
            elif ball.type == 2:
                state.score = max(0, state.score - 1)
            else:
                state.score += 1

            if state.score >= state.next_level_up_score:
                state.balls.append(Ball())
                state.speed = state.initial_speed
                self.width = 40
                state.next_level_up_score += 10
        else:
            # missed
            state.misses += 1
            if state.misses >= 10:
                state.game_over = True


class App:
    """Encapsulates all game state and logic; no globals."""
    def __init__(self):
        pyxel.init(200, 200, fps=30)
        pyxel.mouse(True)

        # State
        self.initial_speed       = 1.0
        self.speed               = self.initial_speed
        self.score               = 0
        self.misses              = 0
        self.game_over           = False
        self.next_level_up_score = 10

        # Bullet lists
        self.bullet_speed = 5
        self.bullet_xs    = []
        self.bullet_ys    = []

        # Objects
        self.pad   = Pad()
        self.balls = [Ball()]

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over:
            return

        # Update paddle
        self.pad.update()

        # R: reset speed and shrink pad
        if pyxel.btnp(pyxel.KEY_R):
            self.speed = self.initial_speed
            self.pad.width = max(20, self.pad.width - 10)

        # Z: fire bullet
        if pyxel.btnp(pyxel.KEY_Z):
            self.bullet_xs.append(self.pad.x + self.pad.width // 2)
            self.bullet_ys.append(self.pad.y)

        # Update bullets
        for i in reversed(range(len(self.bullet_xs))):
            self.bullet_ys[i] -= self.bullet_speed
            if self.bullet_ys[i] < 0:
                self.bullet_xs.pop(i)
                self.bullet_ys.pop(i)

        # Update balls
        for ball in self.balls:
            hit_bottom = ball.update(self.speed)

            # Bullet-ball collision
            for i in reversed(range(len(self.bullet_xs))):
                dx = self.bullet_xs[i] - ball.x
                dy = self.bullet_ys[i] - ball.y
                if dx*dx + dy*dy < 100:
                    ball.restart()
                    self.bullet_xs.pop(i)
                    self.bullet_ys.pop(i)
                    self.score += 1
                    break

            # Ball reached bottom
            if hit_bottom:
                self.pad.catch(ball, self)
                self.speed += 0.1

    def draw(self):
        if self.game_over:
            pyxel.cls(7)
            pyxel.text(70,  90, "GAME OVER",        8)
            pyxel.text(60, 110, f"Final Score: {self.score}", 7)
            return

        pyxel.cls(7)

        # Draw bullets
        for x, y in zip(self.bullet_xs, self.bullet_ys):
            pyxel.rect(x-1, y, 2, 6, 12)

        # Draw balls
        for ball in self.balls:
            ball.draw()

        # Draw paddle
        self.pad.draw()

        # HUD
        pyxel.text(5,  5, f"Score:   {self.score}",  0)
        pyxel.text(5, 15, f"Misses: {self.misses}", 0)
        pyxel.text(5, 25, "R: slow+shrink pad",    0)
        pyxel.text(5, 35, "Z: shoot bullet",        0)


# Start the application
App()