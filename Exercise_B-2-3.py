import pyxel

pyxel.init(200, 200)
pyxel.cls(7)  # Light gray background

cx, cy = 100, 100
step = 2

for idx, pos in enumerate(range(0, 201, step)):
    # Top wedge: center → top edge
    pyxel.line(cx, cy, pos, 0, idx % 16)
    # Right wedge: center → right edge
    pyxel.line(cx, cy, 200, pos, (idx + 4) % 16)
    # Bottom wedge: center → bottom edge
    pyxel.line(cx, cy, 200 - pos, 200, (idx + 8) % 16)
    # Left wedge: center → left edge
    pyxel.line(cx, cy, 0, 200 - pos, (idx + 12) % 16)

pyxel.show()