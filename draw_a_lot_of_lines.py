import pyxel

pyxel.init(200, 200)
pyxel.cls(7)

for a in range(0, 101, 10):  # 左上辺から始まる線
    pyxel.line(a, 0, a + 100, 200, 0)

pyxel.show()