import pyxel

pyxel.init(200, 200)
pyxel.cls(7)
for a in range(0, 201, 10):
    pyxel.line(0, a, 200, 200-a, 0)
    pyxel.flip()
pyxel.show()