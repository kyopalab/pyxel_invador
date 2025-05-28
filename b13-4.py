# Burst of a bubble

import math    # provides mathematical functions
import random  # random number generation for bubble properties
import pyxel   # Pyxel game engine

# Screen dimensions define the window size
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

# Bubble behavior configuration
BUBBLE_MAX_SPEED     = 1.8   # Maximum speed (pixels per frame)
BUBBLE_INITIAL_COUNT = 50    # Initial bubble count
BUBBLE_EXPLODE_COUNT = 11    # Number of bubbles to spawn on explode (unused here)

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
        """Initialize at random top-X, zero Y, random angle & type."""
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
        # Advance position
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
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.mouse(True)

        # Create initial bubbles
        self.bubbles = [Bubble() for _ in range(BUBBLE_INITIAL_COUNT)]

        # Start the game loop
        pyxel.run(self.update, self.draw)

    def update(self):
        """Update logic called once per frame, including bubble merges."""
        bubble_count = len(self.bubbles)

        # Iterate backwards so we can safely remove bubbles
        for i in range(bubble_count - 1, -1, -1):
            bi = self.bubbles[i]
            bi.update()

            # Compare with earlier bubbles for overlap/merge
            for j in range(i - 1, -1, -1):
                bj = self.bubbles[j]
                dx = bi.pos.x - bj.pos.x
                dy = bi.pos.y - bj.pos.y
                total_r = bi.r + bj.r

                # If they overlap, merge into a new bubble
                if dx*dx + dy*dy < total_r*total_r:
                    new_bubble = Bubble()
                    # combine area to radius
                    new_bubble.r = math.sqrt(bi.r*bi.r + bj.r*bj.r)
                    # weighted position
                    new_bubble.pos.x = (bi.pos.x*bi.r + bj.pos.x*bj.r) / total_r
                    new_bubble.pos.y = (bi.pos.y*bi.r + bj.pos.y*bj.r) / total_r
                    # weighted velocity
                    new_bubble.vel.x = (bi.vel.x*bi.r + bj.vel.x*bj.r) / total_r
                    new_bubble.vel.y = (bi.vel.y*bi.r + bj.vel.y*bj.r) / total_r

                    self.bubbles.append(new_bubble)
                    # remove the originals
                    del self.bubbles[i]
                    del self.bubbles[j]
                    bubble_count -= 1
                    break

    def draw(self):
        """Render called once per frame."""
        pyxel.cls(0)
        for bubble in self.bubbles:
            bubble.draw()

# Instantiate and run the application
App()