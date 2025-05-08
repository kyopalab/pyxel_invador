

import pyxel

# Window size
WIDTH = 200
HEIGHT = 200

# List to store endpoints of committed lines
committed_lines = []

# Track previous state of the space key to detect release
prev_space_pressed = False

def update():
   global prev_space_pressed

   # Check whether the space key is currently down
   space_pressed = pyxel.btn(pyxel.KEY_SPACE)

   # If the space key was down last frame but is released this frame, commit the line
   if prev_space_pressed and not space_pressed:
       committed_lines.append((pyxel.mouse_x, pyxel.mouse_y))

   # Update previous state for next frame
   prev_space_pressed = space_pressed


def draw():
   # Clear the screen to light gray (palette index 7)
   pyxel.cls(7)

   # Draw all committed lines in black (palette index 0)
   for x2, y2 in committed_lines:
       pyxel.line(0, 0, x2, y2, 0)

   # While holding space, draw a live preview line in black
   if pyxel.btn(pyxel.KEY_SPACE):
       mx = pyxel.mouse_x
       my = pyxel.mouse_y
       pyxel.line(0, 0, mx, my, 0)

# Initialize Pyxel and start the main loop
pyxel.init(WIDTH, HEIGHT)
pyxel.mouse(True)
pyxel.run(update, draw)


