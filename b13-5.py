# Display message

import math    # provides mathematical functions
import random  # random number generation for bubble properties
import pyxel   # Pyxel game engine

# Screen dimensions define the window size
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

# Bubble behavior configuration
BUBBLE_MAX_SPEED     = 1.8   # Maximum speed (pixels per frame)
BUBBLE_INITIAL_COUNT = 50    # Initial bubble count
BUBBLE_EXPLODE_COUNT = 11    # Number of bubbles to spawn when one explodes

class Vec2:
    """Simple 2D vector to hold x, y coordinates or velocities."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Bubble:
    """A moving circle that bounces within the screen bounds."""
    def __init__(self):
        self.restart()

    def restart(self):
        """Initialize at random position, random velocity & color."""
        self.r = random.uniform(3, 10)
        self.pos = Vec2(
            random.uniform(self.r, SCREEN_WIDTH - self.r),
            random.uniform(self.r, SCREEN_HEIGHT - self.r),
        )
        self.vel = Vec2(
            random.uniform(-BUBBLE_MAX_SPEED, BUBBLE_MAX_SPEED),
            random.uniform(-BUBBLE_MAX_SPEED, BUBBLE_MAX_SPEED),
        )
        self.color = random.randint(1, 15)

    def update(self):
        """Move the bubble and bounce off the four screen edges."""
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        # Bounce horizontally
        if self.pos.x < self.r:
            self.pos.x = self.r
            self.vel.x *= -1
        elif self.pos.x > SCREEN_WIDTH - self.r:
            self.pos.x = SCREEN_WIDTH - self.r
            self.vel.x *= -1

        # Bounce vertically
        if self.pos.y < self.r:
            self.pos.y = self.r
            self.vel.y *= -1
        elif self.pos.y > SCREEN_HEIGHT - self.r:
            self.pos.y = SCREEN_HEIGHT - self.r
            self.vel.y *= -1

    def draw(self):
        pyxel.circ(self.pos.x, self.pos.y, self.r, self.color)

class App:
    """Main application class handling setup, update, and draw."""
    def __init__(self):
        # Added caption argument
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.mouse(True)
        # Track whether an explosion has occurred
        self.is_exploded = False

        # Create initial bubbles
        self.bubbles = [Bubble() for _ in range(BUBBLE_INITIAL_COUNT)]

        # Start the game loop
        pyxel.run(self.update, self.draw)

    def update(self):
        """Update logic called once per frame, including explosions and merges."""
        bubble_count = len(self.bubbles)

        # 1) Handle mouse-click explosions
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for i in range(bubble_count - 1, -1, -1):
                b = self.bubbles[i]
                dx = b.pos.x - pyxel.mouse_x
                dy = b.pos.y - pyxel.mouse_y
                if dx*dx + dy*dy < b.r*b.r:
                    # Mark that we've exploded at least once
                    self.is_exploded = True
                    # Explode into smaller bubbles
                    new_r = math.sqrt((b.r*b.r) / BUBBLE_EXPLODE_COUNT)
                    for j in range(BUBBLE_EXPLODE_COUNT):
                        angle = 2*math.pi * j / BUBBLE_EXPLODE_COUNT
                        nb = Bubble()
                        nb.r = new_r
                        nb.pos.x = b.pos.x + (b.r + new_r) * math.cos(angle)
                        nb.pos.y = b.pos.y + (b.r + new_r) * math.sin(angle)
                        nb.vel.x = math.cos(angle) * BUBBLE_MAX_SPEED
                        nb.vel.y = math.sin(angle) * BUBBLE_MAX_SPEED
                        self.bubbles.append(nb)
                    del self.bubbles[i]
                    return  # skip merging on this frame

        # 2) Handle pairwise merges
        bubble_count = len(self.bubbles)
        for i in range(bubble_count - 1, -1, -1):
            bi = self.bubbles[i]
            bi.update()
            for j in range(i - 1, -1, -1):
                bj = self.bubbles[j]
                dx = bi.pos.x - bj.pos.x
                dy = bi.pos.y - bj.pos.y
                total_r = bi.r + bj.r
                if dx*dx + dy*dy < total_r*total_r:
                    nb = Bubble()
                    nb.r = math.sqrt(bi.r*bi.r + bj.r*bj.r)
                    nb.pos.x = (bi.pos.x*bi.r + bj.pos.x*bj.r) / total_r
                    nb.pos.y = (bi.pos.y*bi.r + bj.pos.y*bj.r) / total_r
                    nb.vel.x = (bi.vel.x*bi.r + bj.vel.x*bj.r) / total_r
                    nb.vel.y = (bi.vel.y*bi.r + bj.vel.y*bj.r) / total_r
                    self.bubbles.append(nb)
                    del self.bubbles[i]
                    del self.bubbles[j]
                    break

    def draw(self):
        """Render called once per frame."""
        pyxel.cls(0)
        for bubble in self.bubbles:
            bubble.draw()

        # Show a blinking instruction before the first explosion
        if not self.is_exploded and pyxel.frame_count % 20 < 10:
            pyxel.text(96, 50, "CLICK ON BUBBLE", pyxel.frame_count % 15 + 1)

# Instantiate and run the application
App()