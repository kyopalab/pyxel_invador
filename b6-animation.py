import pyxel

# Initialize a 200×200 window with a title
pyxel.init(200, 200)

# 'a' will serve as both the x- and y-coordinate of the circle
a = 0

def update():
    global a
    # Move the circle diagonally down-right
    a += 1
    # If the circle goes off the right or bottom edge, reset to the upper-left
    if a > pyxel.width or a > pyxel.height:
        a = 0

def draw():
    global a
    # Clear the screen to white (color index 7)
    pyxel.cls(7)
    # Draw a filled circle at (a, a) with radius 10 in black (color index 0)
    pyxel.circ(a, a, 10, 0)

# Start Pyxel's game loop, which calls update() then draw() each frame
pyxel.run(update, draw)