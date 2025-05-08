import pyxel

# Initialize a 200×200 window
pyxel.init(200, 200)

# Clear the screen with color 7 (light gray)
pyxel.cls(7)

# Lists of circle parameters
xs = [10, 70, 145, 150]     # x-coordinates for circles
ys = [50, 160, 30, 130]     # y-coordinates for circles
rs = [5, 20, 10, 15]        # radii for circles
cs = [1, 4, 14, 6]          # color indices for circles

# Draw circles based on the parameter lists
for i in range(len(xs)):
    # Draw a circle at (xs[i], ys[i]) with radius rs[i] and color cs[i]
    pyxel.circ(xs[i], ys[i], rs[i], cs[i])

# Show the drawn frame until the window is closed
pyxel.show()