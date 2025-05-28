# Vec2 class

import pyxel

# Screen dimensions
SCREEN_WIDTH = 256   # The width of the window in pixels
SCREEN_HEIGHT = 256  # The height of the window in pixels

# Bubble parameters (unused in this minimal example)
BUBBLE_MAX_SPEED     = 1.8   # Maximum speed of a bubble
BUBBLE_INITIAL_COUNT = 50    # Number of bubbles at start
BUBBLE_EXPLODE_COUNT = 11    # Number of bubbles to explode

class Vec2:
    """Simple 2D vector for position or movement."""
    def __init__(self, x, y):
        self.x = x  # X coordinate
        self.y = y  # Y coordinate

class App:
    """Main application class handling initialization, update, and draw."""
    def __init__(self):
        # Initialize Pyxel with a window of SCREEN_WIDTH×SCREEN_HEIGHT
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.mouse(True)  # Enable mouse input

        # Store a 2D position for the bubble
        self.pos = Vec2(100, 100)

        # Start the application loop: update() then draw() each frame
        pyxel.run(self.update, self.draw)

    def update(self):
        """Called once per frame before draw(). Here you'd update game logic."""
        # Example: move the bubble to follow the mouse
        # self.pos.x, self.pos.y = pyxel.mouse_x, pyxel.mouse_y
        pass

    def draw(self):
        """Called once per frame after update(). Handle all rendering here."""
        pyxel.cls(0)  # Clear the screen with color 0 (black)
        # Draw a circle at self.pos with radius 30 and color 7 (light gray)
        pyxel.circ(self.pos.x, self.pos.y, 30, 7)

# Create and run the App
App()