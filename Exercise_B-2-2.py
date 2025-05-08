import pyxel

pyxel.init(200, 200)
pyxel.cls(7)  # Set background color to light gray (color 7)

# Diagonal crossing lines (from top edge to left edge)
for i in range(0, 201, 10):
    pyxel.line(200 - i, 0, 0, i, 0)

pyxel.show()