import pyxel

# Window dimensions
WIDTH = 200
HEIGHT = 200

# State variables
press_count = 0           # Counts how many times Space has been pressed
start_x = 0               # Starting x of the current line
start_y = 0               # Starting y of the current line
committed_line = None     # Holds the fixed line as a tuple (x0, y0, x1, y1)

def update():
    global press_count, start_x, start_y, committed_line

    # On each Space key press, toggle between live-draw mode and commit mode
    if pyxel.btnp(pyxel.KEY_SPACE):
        press_count += 1

        if press_count % 2 == 1:
            # Odd press: begin a new live line from the current mouse position
            start_x = pyxel.mouse_x
            start_y = pyxel.mouse_y
            # Clear any previously committed line
            committed_line = None
        else:
            # Even press: fix the line at the moment of pressing Space
            end_x = pyxel.mouse_x
            end_y = pyxel.mouse_y
            committed_line = (start_x, start_y, end_x, end_y)

def draw():
    pyxel.cls(7)  # Clear the screen to light gray (palette index 7)

    # Draw the fixed, committed line if it exists
    if committed_line is not None:
        x0, y0, x1, y1 = committed_line
        pyxel.line(x0, y0, x1, y1, 0)  # Black line (palette index 0)

    # If we're in live-draw mode (odd-numbered press), draw the preview line
    if press_count % 2 == 1:
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        pyxel.line(start_x, start_y, mx, my, 0)  # Black preview line

# Initialize Pyxel and start the loop
pyxel.init(WIDTH, HEIGHT)
pyxel.run(update, draw)