# Fusion of bubbles

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
        self.x = x  # X component
        self.y = y  # Y component

class Bubble:
    """A moving circle that bounces within the screen bounds."""
    def __init__(self):
        # Random radius between 3 and 10 pixels
        self.r = random.uniform(3, 10)
        # Random starting position, clamped so the bubble is fully on screen
        self.pos = Vec2(
            random.uniform(self.r, SCREEN_WIDTH  - self.r),
            random.uniform(self.r, SCREEN_HEIGHT - self.r),
        )
        # Random velocity vector, each component in ±BUBBLE_MAX_SPEED
        self.vel = Vec2(
            random.uniform(-BUBBLE_MAX_SPEED, BUBBLE_MAX_SPEED),
            random.uniform(-BUBBLE_MAX_SPEED, BUBBLE_MAX_SPEED),
        )
        # Random color index between 1 and 15
        self.color = random.randint(1, 15)

    def update(self):
        """Move the bubble and bounce it off each window edge."""
        # Advance position by velocity
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        # Bounce off left edge
        if self.vel.x < 0 and self.pos.x < self.r:
            self.vel.x *= -1
        # Bounce off right edge
        if self.vel.x > 0 and self.pos.x > SCREEN_WIDTH - self.r:
            self.vel.x *= -1

        # Bounce off top edge
        if self.vel.y < 0 and self.pos.y < self.r:
            self.vel.y *= -1
        # Bounce off bottom edge
        if self.vel.y > 0 and self.pos.y > SCREEN_HEIGHT - self.r:
            self.vel.y *= -1

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
        """Update logic called once per frame."""
        # Update each bubble’s position and bounce logic
        for bubble in self.bubbles:
            bubble.update()

    def draw(self):
        """Render called once per frame."""
        pyxel.cls(0)
        # Draw all bubbles on the screen
        for bubble in self.bubbles:
            pyxel.circ(bubble.pos.x, bubble.pos.y, bubble.r, bubble.color)

# Instantiate and run the application
App()