import pyxel

# Initialize a 200×200 window
pyxel.init(200, 200)
# Clear the screen with color 7 (light gray)
pyxel.cls(7)

# Draw diagonal lines in steps to create an animation effect
for a in range(0, 101, 10):
    # Draw a line from (a, 0) to (a+100, 200) with color 0 (black)
    pyxel.line(a, 0, a + 100, 200, 0)
    # Immediately update the display to show this line
    pyxel.flip()

# Keep the window open until the user closes it
pyxel.show()