import pyxel

# Window dimensions
WIDTH = 200
HEIGHT = 200

# Circle properties
x = 0                  # current x position
y = 0                  # current y position
radius = 10            # circle radius

# Movement direction: 1 means down-right, -1 means up-left
dx = 1
dy = 1

def update():
    global x, y, dx, dy

    # Move the circle
    x += dx
    y += dy

    # If we reach or pass the lower-right corner, reverse direction
    if x >= WIDTH or y >= HEIGHT:
        dx = -1
        dy = -1

    # If we reach or pass the upper-left corner, reverse direction
    if x <= 0 or y <= 0:
        dx = 1
        dy = 1

def draw():
    # Clear screen to light gray (color index 7)
    pyxel.cls(7)
    # Draw the circle in black (color index 0)
    pyxel.circ(x, y, radius, 0)

# Initialize and start the Pyxel application
pyxel.init(WIDTH, HEIGHT)
pyxel.run(update, draw)