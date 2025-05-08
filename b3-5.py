import pyxel

pyxel.init(200, 200)
pyxel.cls(7)
for b in range(10, 200, 20):
    for a in range(10, 200, 20):
        pyxel.circ(a, b, 10, 0)
pyxel.show()