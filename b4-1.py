import pyxel

pyxel.init(200, 200)
pyxel.cls(7)

for a in range(10, 100, 20):
    pyxel.circ(a, 10, 10, 0)

for a in range(10, 80, 20):
    pyxel.circ(a, 30, 10, 0)

for a in range(10, 60, 20):
    pyxel.circ(a, 50, 10, 0)

for a in range(10, 40, 20):
    pyxel.circ(a, 70, 10, 0)

for a in range(10, 21, 20):
    pyxel.circ(a, 90, 10, 0)

pyxel.show()