# Created by Kyopan

import pyxel

# Definition of screen size and constants used in the game
SCREEN_WIDTH  = 512
SCREEN_HEIGHT = 512

# Constants for object size, color, etc.
PLAYER_WIDTH  = 16
PLAYER_HEIGHT = 8
PLAYER_COLOR  = 11  # Player spaceship color (11: green)

BULLET_WIDTH  = 2
BULLET_HEIGHT = 8
BULLET_COLOR  = 7   # Bullet color (7: white)

ENEMY_WIDTH   = 8
ENEMY_HEIGHT  = 8
ENEMY_COLOR   = 10  # Enemy alien color (10: yellow)

# Enemy movement speed and drop distance
ENEMY_X_SPEED = 2    # Enemy horizontal movement speed
ENEMY_DROP    = 10   # Distance (in pixels) enemies drop when they reach the edge

BULLET_SPEED  = 4    # Bullet movement speed (pixels per frame moving upwards)

# Player (ship) class
class Player:
    def __init__(self, x: int, y: int):
        self.x = x  # Spaceship's top-left X coordinate
        self.y = y  # Spaceship's top-left Y coordinate
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.color = PLAYER_COLOR

    def update(self):
        # Move the player position based on mouse X coordinate (adjusted to center on cursor)
        target_x = pyxel.mouse_x - self.w // 2
        # Adjust position to stay within the screen
        if target_x < 0:
            target_x = 0
        if target_x > pyxel.width - self.w:
            target_x = pyxel.width - self.w
        self.x = target_x
        # ※ Y coordinate is fixed (no vertical movement)

    def draw(self):
        # Draw the spaceship as a triangle (base down, apex up)
        x1 = self.x
        y1 = self.y + self.h  # Y coordinate of the base (bottom of the spaceship)
        x2 = self.x + self.w
        y2 = self.y + self.h  # Right side of the base
        x3 = self.x + self.w // 2
        y3 = self.y           # Apex (tip of the spaceship)
        pyxel.tri(x1, y1, x2, y2, x3, y3, self.color)

# Class representing a bullet
class Bullet:
    def __init__(self, x: int, y: int):
        self.x = x  # Bullet's top-left X coordinate
        self.y = y  # Bullet's top-left Y coordinate
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.color = BULLET_COLOR
        self.active = True  # Flag indicating if the bullet is active

    def update(self):
        # Move the bullet upwards
        self.y -= BULLET_SPEED
        # Deactivate if it goes off-screen
        if self.y + self.h < 0:
            self.active = False

    def draw(self):
        # Draw the bullet as a rectangle
        pyxel.rect(self.x, self.y, self.w, self.h, self.color)

# Class for enemy aliens
class Enemy:
    def __init__(self, x: int, y: int):
        self.x = x  # Enemy's top-left X coordinate
        self.y = y  # Enemy's top-left Y coordinate
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.color = ENEMY_COLOR
        self.alive = True  # Alive flag

    def draw(self):
        # Draw the enemy as a rectangle
        pyxel.rect(self.x, self.y, self.w, self.h, self.color)

# Class managing the entire game
class Game:
    def __init__(self):
        # Initialize Pyxel
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.mouse(True)  # Show mouse cursor

        # Sound and BGM settings
        # Sound IDs:
        # 0 = Bullet shot sound, 1 = Enemy defeat sound, 2 = Game over sound, 3 = BGM, 4 = Victory sound
        pyxel.sounds[0].set("c4c3", "p", "66", "s", 10)  # High sound descending slightly to lower sound
        pyxel.sounds[1].set("c1",  "n", "6",  "f", 10)   # Noise sound (explosion sound, fade-out effect)
        pyxel.sounds[2].set("c2",  "t", "7",  "n", 30)   # Lower single note (for game over)
        pyxel.sounds[3].set("c4e4g4e4", "p", "4444", "n", 15)  # Simple 4-note loop melody (BGM)
        pyxel.sounds[4].set("c4c4", "p", "66", "n", 10)  # Ascending 2-note (for victory)

        # Initialize game state
        self.reset_game()
        # Start Pyxel's main loop
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """Reset state at game start/restart"""
        # Initialize player (placed near the center bottom of the screen)
        player_start_x = SCREEN_WIDTH // 2
        player_start_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 20  # Positioned 20 pixels above the bottom
        self.player = Player(player_start_x, player_start_y)

        # Initial placement of enemy cluster (arranged in multiple rows and columns)
        self.enemies = []
        cols = 5   # Number of enemy columns
        rows = 3   # Number of enemy rows
        start_x = 60   # Top-left X coordinate of the first enemy
        start_y = 60   # Top-left Y coordinate of the first enemy
        spacing_x = 30  # Horizontal spacing
        spacing_y = 20  # Vertical spacing
        for j in range(rows):
            for i in range(cols):
                x = start_x + i * spacing_x
                y = start_y + j * spacing_y
                self.enemies.append(Enemy(x, y))
        # No bullets exist initially
        self.bullet = None

        # Reset score
        self.score = 0

        # Current movement direction of enemies (1: right, -1: left)
        self.enemy_direction = 1

        # Game over related flags
        self.game_over = False
        self.win = False

        # Start BGM playback (loop)
        pyxel.play(3, 3, loop=True)

    def update(self):
        # Press Q key to exit the game (close window)
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.game_over:
            # During game over, press R key to restart
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        # Update player position (following the mouse)
        self.player.update()

        # Bullet firing process (when left mouse button is pressed)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.bullet is None or not self.bullet.active:
                # Fire a new bullet from the player spaceship
                bullet_x = self.player.x + (self.player.w // 2) - (BULLET_WIDTH // 2)
                bullet_y = self.player.y - BULLET_HEIGHT
                self.bullet = Bullet(bullet_x, bullet_y)
                # Play firing sound (on channel 0)
                pyxel.play(0, 0)

        # Update existing bullet if it exists
        if self.bullet is not None and self.bullet.active:
            self.bullet.update()
            # If bullet becomes inactive (reaches off-screen), delete the object
            if not self.bullet.active:
                self.bullet = None

        # Enemy movement process
        if len(self.enemies) > 0:
            # Check if reaching the edge of the screen
            # Calculate the leftmost and rightmost of the current enemy cluster
            min_x = min(enemy.x for enemy in self.enemies)
            max_x = max(enemy.x for enemy in self.enemies) + ENEMY_WIDTH
            # If moving right and the rightmost enemy reaches the right edge of the screen
            if self.enemy_direction == 1 and max_x >= pyxel.width:
                # Move all enemies down and reverse direction
                for enemy in self.enemies:
                    enemy.y += ENEMY_DROP
                self.enemy_direction = -1
            # If moving left and the leftmost enemy reaches the left edge of the screen
            elif self.enemy_direction == -1 and min_x <= 0:
                for enemy in self.enemies:
                    enemy.y += ENEMY_DROP
                self.enemy_direction = 1
            else:
                # Normally move horizontally in the current direction
                for enemy in self.enemies:
                    enemy.x += ENEMY_X_SPEED * self.enemy_direction

        # Collision detection between bullet and enemies
        if self.bullet is not None:
            for enemy in list(self.enemies):  # Loop using a copy of the list
                if (self.bullet is not None and 
                    enemy.alive and 
                    # Rectangle collision detection (bullet and enemy)
                    self.bullet.x < enemy.x + enemy.w and 
                    self.bullet.x + self.bullet.w > enemy.x and 
                    self.bullet.y < enemy.y + enemy.h and 
                    self.bullet.y + self.bullet.h > enemy.y):
                    # If collision occurs
                    enemy.alive = False
                    self.enemies.remove(enemy)  # Remove enemy from the list
                    self.bullet.active = False  # Remove bullet
                    self.bullet = None
                    self.score += 1
                    # Play explosion sound (on channel 1)
                    pyxel.play(1, 1)
                    break  # Prevent multiple enemies from being destroyed by a single bullet

        # Game over/victory detection
        if not self.game_over:
            # Have enemies reached the bottom of the screen (player's Y coordinate)?
            for enemy in self.enemies:
                if enemy.y + enemy.h >= self.player.y:
                    # Enemies have invaded the player line => Game Over (defeat)
                    self.game_over = True
                    self.win = False
                    # Stop BGM and play game over sound
                    pyxel.stop()
                    pyxel.play(2, 2)  # Play game over sound on channel 2
                    break
            # Have all enemies been defeated?
            if not self.game_over and len(self.enemies) == 0:
                # All enemies defeated => Player victory
                self.game_over = True
                self.win = True
                pyxel.stop()
                pyxel.play(2, 4)  # Play victory sound (short fanfare) on channel 2

    def draw(self):
        # Clear background to black
        pyxel.cls(0)

        # Draw all objects
        self.player.draw()
        if self.bullet is not None and self.bullet.active:
            self.bullet.draw()
        for enemy in self.enemies:
            if enemy.alive:
                enemy.draw()

        # Display score (white text)
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)

        # Display message during game over
        if self.game_over:
            msg = "YOU WIN!" if self.win else "GAME OVER"
            color = 10 if self.win else 8  # Yellow for victory, red for defeat
            text_width = len(msg) * 4  # pyxel.text uses 4px width per character (default font)
            x = (pyxel.width - text_width) // 2
            y = pyxel.height // 2
            pyxel.text(x, y, msg, color)
            # Restart instructions
            pyxel.text(x - 20, y + 10, "Press R to Restart", 7)

# Start the game (main entry point)
if __name__ == "__main__":
    Game()