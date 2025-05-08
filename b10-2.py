import pyxel

# Initialize a 200×200 window
pyxel.init(200, 200)
# Enable mouse input
pyxel.mouse(True)

# Lists to store circle parameters
xs = []  # x-positions
ys = []  # y-positions
rs = []  # radii
cs = []  # colors

def update():
    global xs, ys, rs, cs
    # When the space key is pressed, record current mouse position and randomize size/color
    if pyxel.btnp(pyxel.KEY_SPACE):
        xs.append(pyxel.mouse_x)
        ys.append(pyxel.mouse_y)
        rs.append(pyxel.rndi(5, 20))   # random radius between 5 and 20
        cs.append(pyxel.rndi(0, 15))   # random color index between 0 and 15

def draw():
    global xs, ys, rs, cs
    # Clear the screen with color 7 (light gray)
    pyxel.cls(7)
    # Draw all stored circles
    for i in range(len(xs)):
        # Draw a circle at (xs[i], ys[i]) with radius rs[i] and color cs[i]
        pyxel.circ(xs[i], ys[i], rs[i], cs[i])

# Start the Pyxel application, calling update() and draw() each frame
pyxel.run(update, draw)