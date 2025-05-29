from random import randint
import pyxel


class Background:
    def __init__(self):
        self.clouds = [(randint(0, 200), randint(0, 120)) for _ in range(20)]

    def update(self):
        self.clouds = [(x - 1 if x > -20 else 220, y) for x, y in self.clouds]

    def draw(self):
        for x, y in self.clouds:
            pyxel.pset(x, y, 7)


class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.background = Background()
        self.player_x = 72
        self.player_y = 100
        self.player_vy = 0
        self.score = 0
        self.near_cloud = [(randint(0, 160), randint(0, 120)) for _ in range(10)]
        # Initialize moving floor segments (x, y, active)
        self.floor = [(i * 60, randint(8, 104), True) for i in range(4)]
        pyxel.run(self.update, self.draw)

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += 2

        self.player_vy += 1
        self.player_y += self.player_vy

        if self.player_y > 100:
            self.player_y = 100
            self.player_vy = 0

    def update_floor(self, x, y, is_active):
        # If the floor segment is currently active (solid)
        if is_active:
            # Check collision with player from above
            if (
                self.player_x + 16 >= x
                and self.player_x <= x + 40
                and self.player_y + 16 >= y
                and self.player_y <= y + 8
                and self.player_vy > 0
            ):
                is_active = False
                self.score += 10
                self.player_vy = -12
                pyxel.play(3, 3)
        else:
            # After being stepped on, sink downward
            y += 6

        # Move floor leftward
        x -= 4

        # Wrap around when off-screen
        if x < -40:
            x += 240
            y = randint(8, 104)
            is_active = True

        return x, y, is_active

    def update(self):
        self.background.update()
        # Update floor segments each frame
        for i, seg in enumerate(self.floor):
            self.floor[i] = self.update_floor(*seg)
        self.update_player()

    def draw(self):
        pyxel.cls(0)
        self.background.draw()
        for x, y in self.near_cloud:
            pyxel.pset(x, y, 10)
        # draw floors
        for x, y, is_active in self.floor:
            pyxel.blt(x, y, 0, 0, 16, 40, 8, 12)
        pyxel.rect(self.player_x, self.player_y, 16, 16, 11)
        pyxel.text(5, 5, f"Score: {self.score}", 7)


App()
