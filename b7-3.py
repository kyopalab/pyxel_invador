import pyxel

# Window size
WIDTH = 200
HEIGHT = 200

# List of committed lines: each is (x0, y0, x1, y1)
committed_lines = []

# Drawing state:
# 0 = next press sets the start point
# 1 = next press sets the end point (live preview shown)
state = 0

# Current starting point of the line
start_x = 0
start_y = 0

def update():
    global state, start_x, start_y, committed_lines

    # Detect when the Space key is pressed
    if pyxel.btnp(pyxel.KEY_SPACE):
        if state == 0:
            # On first press: fix the start point and switch to end-point mode
            start_x = pyxel.mouse_x
            start_y = pyxel.mouse_y
            state = 1
        else:
            # On second press: fix the end point, commit the line, and return to start-point mode
            end_x = pyxel.mouse_x
            end_y = pyxel.mouse_y
            committed_lines.append((start_x, start_y, end_x, end_y))
            state = 0

def draw():
    # Clear background to light gray
    pyxel.cls(7)

    # Draw all committed lines
    for x0, y0, x1, y1 in committed_lines:
        pyxel.line(x0, y0, x1, y1, 0)

    # If in end-point mode, draw a live preview line to the current mouse position
    if state == 1:
        mx = pyxel.mouse_x
        my = pyxel.mouse_y
        pyxel.line(start_x, start_y, mx, my, 0)

# Initialize Pyxel and start the application
pyxel.init(WIDTH, HEIGHT)
pyxel.mouse(True)
pyxel.run(update, draw)