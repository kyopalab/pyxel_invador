import pyxel

class App:
    def __init__(self):
        # Initialize Pyxel window at 160×120 pixels
        pyxel.init(160, 120)
        # Load assets (images, sounds) from the resource file
        pyxel.load("assets/jump_game.pyxres")
        # Start background music track 0 on loop
        pyxel.playm(0, loop=True)
        # Begin the application loop, calling update() and draw() each frame
        pyxel.run(self.update, self.draw)

    def update(self):
        # Placeholder for game state updates (e.g., input handling, physics)
        pass

    def draw(self):
        # Clear the screen with palette color 12 (background)
        pyxel.cls(12)
        # Draw a 16×16 sprite from image bank 0 at screen position (80, 60)
        # The sprite source rectangle starts at (16, 0) in the bank
        # Color index 12 in the sprite is treated as transparent
        pyxel.blt(
            80,  # X coordinate on the screen
            60,  # Y coordinate on the screen
            0,   # Image bank index
            16,  # X coordinate in the image bank
            0,   # Y coordinate in the image bank
            16,  # Width of the sprite to blit
            16,  # Height of the sprite to blit
            12,  # Transparent color index (color key)
        )

# Create and run the app
App()