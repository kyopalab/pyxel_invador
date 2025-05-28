# Bubble class

import math                # Math functions (unused here but available)
import random              # Random number generation
import pyxel               # Pyxel game library

# Screen dimensions
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

# Bubble behavior configuration
BUBBLE_MAX_SPEED     = 1.8   # Maximum speed (pixels per frame)
BUBBLE_INITIAL_COUNT = 50    # Initial bubble count (unused in single‐bubble demo)
BUBBLE_EXPLODE_COUNT = 11    # Number of bubbles to spawn on explode (unused here)

class Vec2:
    """Simple 2D vector to hold x,y coordinates or velocities."""
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
    """Main application class: sets up Pyxel and runs the game loop."""
    def __init__(self):
        # Initialize Pyxel window
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.mouse(True)  # Enable mouse input (not used in this demo)

        # Create a single bubble instance
        self.bubble = Bubble()

        # Start the Pyxel run loop, calling update() then draw() each frame
        pyxel.run(self.update, self.draw)

    def update(self):
        """Called every frame to update game logic."""
        # Simply update the bubble’s position and bounce logic
        self.bubble.update()

    def draw(self):
        """Called every frame to render the scene."""
        pyxel.cls(0)  # Clear the screen with color 0 (black)
        # Draw the bubble: position, radius, and color
        pyxel.circ(
            self.bubble.pos.x,
            self.bubble.pos.y,
            self.bubble.r,
            self.bubble.color
        )

# Instantiate and run the application
App()