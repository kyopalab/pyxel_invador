import pyxel

pyxel.init(200,200)

a = 0

def update():
    global a
    a += 1

def draw():
    global a
    pyxel.cls(7)
    pyxel.circ(a, a, 10, 0)

pyxel.run(update, draw)