

import pyxel
from random import random

# Scene identifiers
SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

# Starfield configuration
STAR_COUNT = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5

class Background:
    """Starfield background with vertical scrolling stars."""
    def __init__(self):
        self.star_list = []
        for _ in range(STAR_COUNT):
            self.star_list.append((
                random() * pyxel.width,
                random() * pyxel.height,
                random() * 1.5 + 1
            ))

    def update(self):
        """Move stars downward and wrap to top when reaching bottom."""
        for i, (x, y, speed) in enumerate(self.star_list):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.star_list[i] = (x, y, speed)

    def draw(self):
        """Render each star as a single pixel with color based on speed."""
        for x, y, speed in self.star_list:
            color = STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW
            pyxel.pset(x, y, color)

class App:
    """Main application class handling scenes and background."""
    def __init__(self):
        pyxel.init(120, 160)
        self.scene = SCENE_TITLE
        self.score = 0
        self.background = Background()
        pyxel.run(self.update, self.draw)

    def update(self):
        """Update background and current scene logic each frame."""
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.background.update()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        """Proceed to play scene when Return is pressed."""
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        """Proceed to game over scene when Return is pressed."""
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_GAMEOVER

    def update_gameover_scene(self):
        """Restart game when Return is pressed."""
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY
            self.score = 0

    def draw(self):
        """Render background, active scene, and score."""
        pyxel.cls(0)
        self.background.draw()

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

    def draw_title_scene(self):
        pyxel.text(35, 66, "Pyxel Shooter", pyxel.frame_count % 16)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_play_scene(self):
        pyxel.text(39, 66, "Now Playing", 13)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_gameover_scene(self):
        pyxel.text(43, 66, "GAME OVER", 8)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

App()