import pyxel

# Initialize a 200×200 window with 5 frames per second
pyxel.init(200, 200, fps=5)
# Clear the screen with color 7 (light gray)
pyxel.cls(7)

# Draw 10 random circles
for a in range(10):
    # Pick a random x position between 0 and 199
    x = pyxel.rndi(0, 199)
    # Pick a random y position between 0 and 199
    y = pyxel.rndi(0, 199)
    # Pick a random radius between 5 and 20
    r = pyxel.rndi(5, 20)
    # Pick a random color index between 0 and 15
    c = pyxel.rndi(0, 15)
    # Draw the circle
    pyxel.circ(x, y, r, c)
    # Immediately update the display to show this circle
    pyxel.flip()

# Keep the window open until closed
pyxel.show()