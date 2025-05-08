import pyxel

pyxel.init(200, 200)
pyxel.cls(7)
for a in range(10, 200, 20):
    pyxel.circ(a, 10, 10, 0)
pyxel.show()