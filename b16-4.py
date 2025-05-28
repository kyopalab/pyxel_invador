


import pyxel

# Bullet configuration
BULLET_WIDTH = 2
BULLET_HEIGHT = 8
BULLET_COLOR = 11
BULLET_SPEED = 4

bullet_list = []

def update_list(lst):
    for elem in lst:
        elem.update()

def draw_list(lst):
    for elem in lst:
        elem.draw()

def cleanup_list(lst):
    i = 0
    while i < len(lst):
        if not lst[i].alive:
            lst.pop(i)
        else:
            i += 1


# --- (rest of the code, including Player class, Bullet class, App, etc.) ---

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_COLOR = 10

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.alive = True

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 2
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 2
        self.x = max(0, min(self.x, pyxel.width - self.w))
        self.y = max(0, min(self.y, pyxel.height - self.h))
        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet(
                self.x + (PLAYER_WIDTH - BULLET_WIDTH) / 2,
                self.y - BULLET_HEIGHT / 2
            )
            pyxel.play(0, 0)

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, PLAYER_COLOR)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.alive = True
        bullet_list.append(self)

    def update(self):
        self.y -= BULLET_SPEED
        if self.y + self.h - 1 < 0:
            self.alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)


class App:
    def __init__(self):
        pyxel.init(120, 160)
        self.player = Player(pyxel.width // 2 - PLAYER_WIDTH // 2, pyxel.height - PLAYER_HEIGHT - 8)
        # Fill the player sprite in image bank 0 with solid PLAYER_COLOR
        color_hex = format(PLAYER_COLOR, 'x')
        row_data = color_hex * PLAYER_WIDTH
        data = [row_data] * PLAYER_HEIGHT
        pyxel.images[0].set(0, 0, data)
        pyxel.sound(0).set("a3a2c1a1", "p", "7", "s", 5)
        self.scene = "PLAY"
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.scene == "PLAY":
            self.update_play_scene()
        elif self.scene == "GAMEOVER":
            self.update_gameover_scene()

    def update_play_scene(self):
        update_list(bullet_list)
        cleanup_list(bullet_list)
        self.player.update()
        # (other game logic goes here)

    def update_gameover_scene(self):
        update_list(bullet_list)
        cleanup_list(bullet_list)
        if pyxel.btnp(pyxel.KEY_ENTER):
            bullet_list.clear()
            self.scene = "PLAY"
        # (other gameover logic)

    def draw(self):
        pyxel.cls(0)
        if self.scene == "PLAY":
            self.draw_play_scene()
        elif self.scene == "GAMEOVER":
            self.draw_gameover_scene()

    def draw_play_scene(self):
        self.player.draw()
        draw_list(bullet_list)
        # (draw other objects)

    def draw_gameover_scene(self):
        draw_list(bullet_list)
        # (draw gameover text, etc.)


App()