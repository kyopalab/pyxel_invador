import pyxel

pyxel.init(200,200)

def update():
   pass

def draw():
   pyxel.cls(7)
   pyxel.circ(pyxel.mouse_x, pyxel.mouse_y, 10, 0)

pyxel.run(update, draw)

