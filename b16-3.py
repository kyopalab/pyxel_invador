import pyxel
from random import random

# Scene identifiers
SCENE_TITLE    = 0
SCENE_PLAY     = 1
SCENE_GAMEOVER = 2

# Starfield configuration
STAR_COUNT      = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW  = 5

# Player configuration
PLAYER_WIDTH   = 8
PLAYER_HEIGHT  = 8
PLAYER_SPEED   = 2

class Vec2:
    """Simple 2D vector to hold x, y coordinates."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Background:
    """Starfield background with vertical scrolling stars."""
    def __init__(self):
        self.star_list = [
            (random() * pyxel.width,
             random() * pyxel.height,
             random() * 1.5 + 1)
            for _ in range(STAR_COUNT)
        ]

    def update(self):
        """Move stars downward and wrap to top when reaching bottom."""
        new_list = []
        for x, y, speed in self.star_list:
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            new_list.append((x, y, speed))
        self.star_list = new_list

    def draw(self):
        """Render each star as a single pixel with color based on speed."""
        for x, y, speed in self.star_list:
            color = STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW
            pyxel.pset(x, y, color)

class Player:
    """Player controlled sprite."""
    def __init__(self, x, y):
        self.x     = x
        self.y     = y
        self.w     = PLAYER_WIDTH
        self.h     = PLAYER_HEIGHT
        self.alive = True

    def update(self):
        """Move player in response to cursor keys, clamped to screen."""
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += PLAYER_SPEED

        self.x = max(0, min(self.x, pyxel.width - self.w))
        self.y = max(0, min(self.y, pyxel.height - self.h))

    def draw(self):
        """Draw the player sprite from image bank 0."""
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)


class App:
    """Main application class handling scenes, background, and player."""
    def __init__(self):
        pyxel.init(120, 160)
        # Define the player sprite in bank 0
        pyxel.image(0).set(
            0, 0,
            [
                "00c00c00",
                "0c7007c0",
                "0c7007c0",
                "c703b07c",
                "77033077",
                "785cc587",
                "85c77c58",
                "0c0880c0",
            ]
        )

        self.scene      = SCENE_TITLE
        self.score      = 0
        self.background = Background()
        self.player     = Player(pyxel.width / 2, pyxel.height - 20)

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
        """During play, update player and wait for Return to gameover."""
        self.player.update()
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_GAMEOVER

    def update_gameover_scene(self):
        """Restart game state when Return is pressed."""
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene  = SCENE_PLAY
            self.score  = 0
            # Reset player position
            self.player.x = pyxel.width  / 2
            self.player.y = pyxel.height - 20

    def draw(self):
        """Render background, active scene, player, and HUD."""
        pyxel.cls(0)
        self.background.draw()

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        else:
            self.draw_gameover_scene()

        # Draw score at top
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

    def draw_title_scene(self):
        pyxel.text(35, 66, "Pyxel Shooter",     pyxel.frame_count % 16)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_play_scene(self):
        """During play, draw player sprite."""
        self.player.draw()
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_gameover_scene(self):
        pyxel.text(43, 66, "GAME OVER",        8)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)


# Start the application
App()