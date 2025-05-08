import pyxel

pyxel.init(200, 200)
pyxel.cls(7)
for a in range(10, 200, 20):
    if a <= 40:
        pyxel.circ(a, 10, 10, 2)
    elif a <= 100:
        pyxel.circ(a, 10, 10, 3)
    elif a <= 160:
        pyxel.circ(a, 10, 10, 6)
    else:
        pyxel.circ(a, 10, 10, 14)
pyxel.show()
