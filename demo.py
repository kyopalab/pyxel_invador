# -----------------------------------------------------------------------------
# File:    demo.py
# Project: FIT2 2025
# Author:  Kyopan
# Date:    2025-06-25
#
# Description:
#  Space invador game demo showcasing advanced features
#
# Usage:
#   pyxel run demo.py
#
# Controls:
#   - Mouse: Move paddle horizontally
#   - Space key: Shoot bullets
#
# Dependencies:
#   - pyxel (https://github.com/kitao/pyxel)
#
# License:
#   MIT License
# -----------------------------------------------------------------------------

import pyxel  # Main Pyxel game engine module
import math   # For trigonometric functions and mathematical calculations
import random # For random value generation
from collections import deque  # For efficient queue operations (mouse trail management)

class Particle:
    """Particle effect class for visual effects
    Represents explosions, muzzle flashes, and other visual effects"""
    
    def __init__(self, x, y, vx, vy, color, life=60):
        """Initialize particle
        Args:
            x, y: Initial position
            vx, vy: Velocity vector
            color: Color (Pyxel 16-color palette)
            life: Lifespan (in frames)
        """
        self.x = x
        self.y = y
        self.vx = vx  # X-direction velocity
        self.vy = vy  # Y-direction velocity
        self.color = color
        self.life = life
        self.max_life = life
    
    def update(self):
        """Update particle state
        Returns:
            bool: Whether the particle is still alive
        """
        self.x += self.vx  # Update position with velocity
        self.y += self.vy
        self.vy += 0.1     # Add gravity effect
        self.life -= 1     # Decrease lifespan
        return self.life > 0

class UltimatePyxelGame:
    """Main game class - Shooting game utilizing advanced Pyxel features"""
    
    def __init__(self):
        """Initialize the game"""
        # pyxel.init: Initialize game screen (width, height, title, FPS)
        pyxel.init(256, 192, title="Ultimate Pyxel Demo", fps=60)
        # pyxel.mouse: Enable mouse cursor display
        pyxel.mouse(True)
        
        # Game state management
        self.scene = "MENU"  # Current scene (MENU/GAME/GAMEOVER)
        self.frame = 0       # Frame counter (for animations)
        
        # Data structures for visual effects
        self.mouse_trails = deque(maxlen=20)  # Mouse trails (max 20 points)
        self.particles = []    # List of particle effects
        self.stars = []        # List of background stars
        self.bullets = []      # List of bullets
        self.enemies = []      # List of enemies
        self.powerups = []     # List of power-up items
        self.explosions = []   # List of explosion effects
        
        # Player information (managed as dictionary)
        self.player = {"x": 128, "y": 150, "vx": 0, "vy": 0, "health": 100}
        self.camera = {"x": 0, "y": 0}  # For camera shake
        
        # Game progression management
        self.score = 0
        self.level = 1
        self.enemy_spawn_timer = 0  # Enemy spawn timer
        self.shake_intensity = 0    # Screen shake intensity
        self.enemies_defeated = 0   # Number of enemies defeated
        self.boss = None           # Boss information
        self.boss_active = False   # Boss battle flag
        
        # Call initialization methods
        self.init_graphics()  # Create sprites
        self.init_audio()     # Set up audio
        self.create_starfield()  # Generate starfield background
        
        # pyxel.run: Start game loop (specify update and draw functions)
        pyxel.run(self.update, self.draw)
    
    def init_graphics(self):
        """Initialize graphics assets - Procedural sprite generation"""
        # pyxel.images[0].cls: Clear image bank 0 (fill with transparent color 0)
        pyxel.images[0].cls(0)
        
        # Player ship sprite (16x16 pixels)
        # Define pixel art with string array (0=transparent, B=color 11)
        ship_data = [
            "0000000000000000",
            "0000000BB0000000",
            "000000BBBB000000",
            "00000BBBBBB00000",
            "0000BB0BB0BB0000",
            "000BB00BB00BB000",
            "00BB000BB000BB00",
            "0BB0000BB0000BB0",
            "BB00000BB00000BB",
            "B000000BB000000B",
            "0000000BB0000000",
            "000000BBBB000000",
            "00000BB00BB00000",
            "0000BB0000BB0000",
            "000BB000000BB000",
            "00B00000000B0000"
        ]
        # Convert string data to pixel data
        for y, row in enumerate(ship_data):
            for x, char in enumerate(row):
                if char == 'B':
                    # pyxel.images[0].pset: Set pixel at specified coordinates in image bank 0
                    pyxel.images[0].pset(x, y, 11)
        
        # Enemy sprite (8x8 pixels) - Placed at x+16 position in image bank
        enemy_data = [
            "00RRRR00",
            "0RR00RR0",
            "RRR00RRR",
            "RRR00RRR",
            "RRRRRRRR",
            "0RR00RR0",
            "R0R00R0R",
            "0RR00RR0"
        ]
        for y, row in enumerate(enemy_data):
            for x, char in enumerate(row):
                if char == 'R':
                    # x+16 to avoid overlap with player sprite
                    pyxel.images[0].pset(x + 16, y, 8)
        
        # Power-up sprite (8x8 pixels) - Placed at x+24 position in image bank
        powerup_data = [
            "00YYYY00",
            "0YYYYYY0",
            "YYYYYYYY",
            "YYY00YYY",
            "YYY00YYY",
            "YYYYYYYY",
            "0YYYYYY0",
            "00YYYY00"
        ]
        for y, row in enumerate(powerup_data):
            for x, char in enumerate(row):
                if char == 'Y':
                    # x+24 to avoid overlap with enemy sprite
                    pyxel.images[0].pset(x + 24, y, 10)
        
        # Boss sprite (32x32 pixels) - Placed at x+32 position in image bank
        boss_data = [
            "00000000RRRRRRRR00000000RRRRRRRR",
            "0000000RRRRRRRRRR0000RRRRRRRRRR0",
            "000000RRRRRRRRRRRR00RRRRRRRRRRRR",
            "00000RRRRRRRRRRRRRRRRRRRRRRRRRR0",
            "0000RRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "000RRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "00RRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "0RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRR0000RRRR0000RRRRRRRRRR",
            "RRRRRRRRRR0000RRRR0000RRRRRRRRRR",
            "RRRRRRRRRR0000RRRR0000RRRRRRRRRR",
            "RRRRRRRRRR0000RRRR0000RRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRR00RRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRR0000RRRRRRRRRRRRRRR",
            "RRRRRRRRRRRR000000RRRRRRRRRRRRRR",
            "RRRRRRRRRRR00000000RRRRRRRRRRRRR",
            "RRRRRRRRRR0000000000RRRRRRRRRRRR",
            "RRRRRRRRR000000000000RRRRRRRRRRR",
            "RRRRRRRR00000000000000RRRRRRRRRR",
            "RRRRRRR0000000000000000RRRRRRRRR",
            "RRRRRR000000000000000000RRRRRRRR",
            "RRRRR00000000000000000000RRRRRRR",
            "RRRR0000000000000000000000RRRRRR",
            "RRR000000000000000000000000RRRRR"
        ]
        for y, row in enumerate(boss_data):
            for x, char in enumerate(row):
                if char == 'R':
                    # Place boss sprite at x+32, y+8
                    pyxel.images[0].pset(x + 32, y + 8, 8)
    
    def init_audio(self):
        """Initialize audio system - Set up sound effects and BGM"""
        # pyxel.sounds[].set: Set sound effects (pitch, tone, volume, effect, length)
        
        # Bullet firing sound (pitch slide effect)
        pyxel.sounds[0].set("c4c3", "p", "64", "s", 8)
        
        # Explosion sound (noise-based)
        pyxel.sounds[1].set("c1", "n", "6", "f", 15)
        
        # Power-up acquisition sound (harmonic melody)
        pyxel.sounds[2].set("c4e4g4c4", "p", "4444", "n", 20)
        
        # Background music melody track (pulse wave)
        pyxel.sounds[3].set("c3e3g3c4e4g4c4e4", "p", "77777777", "n", 60)
        
        # Background music bass track (triangle wave)
        pyxel.sounds[4].set("c2c2g2g2a2a2g2f2", "t", "44444444", "n", 60)
        
        # pyxel.musics[].set: Set 4-channel music (ch0,ch1,ch2,ch3)
        pyxel.musics[0].set([3], [4], [], [])
    
    def create_starfield(self):
        """Generate starfield background - Create random stars for parallax effect"""
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, 255),      # random X coordinate
                'y': random.randint(0, 191),      # random Y coordinate
                'speed': random.uniform(0.5, 3.0),  # random speed
                'color': random.choice([5, 6, 7, 12, 13])  # random color from Pyxel palette
            })
    
    def update(self):
        self.frame += 1
        
        # Mouse trail
        self.mouse_trails.append((pyxel.mouse_x, pyxel.mouse_y))
        
        if self.scene == "MENU":
            self.update_menu()
        elif self.scene == "GAME":
            self.update_game()
        elif self.scene == "GAMEOVER":
            self.update_gameover()
        
        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
        # Update explosions
        self.explosions = [e for e in self.explosions if e['life'] > 0]
        for explosion in self.explosions:
            explosion['life'] -= 1
            explosion['radius'] += 1
    
    def update_menu(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.scene = "GAME"
            pyxel.playm(0, loop=True)
    
    def update_game(self):
        self.update_player()
        self.update_bullets()
        self.update_enemies()
        self.update_powerups()
        self.update_starfield()
        self.update_boss()
        self.check_collisions()
        self.spawn_enemies()
        self.camera_shake()
    
    def update_player(self):
        """Update player state - Handle movement, shooting, and mouse tracking"""
        # get mouse position
        target_x = pyxel.mouse_x
        target_y = pyxel.mouse_y
        
        # Clamp mouse position to screen bounds
        target_x = max(8, min(248, target_x))
        target_y = max(8, min(184, target_y))
        
        # Calculate direction vector to mouse position
        dx = target_x - self.player['x']
        dy = target_y - self.player['y']
        
        # Normalize direction vector
        self.player['vx'] = dx * 0.15  # Adjust speed factor for smoother movement
        self.player['vy'] = dy * 0.15
        
        # Limit player speed
        self.player['x'] += self.player['vx']
        self.player['y'] += self.player['vy']
        
        # space key to shoot
        if self.frame % 5 == 0 and pyxel.btn(pyxel.KEY_SPACE):
            self.bullets.append({
                'x': self.player['x'],
                'y': self.player['y'] - 8,
                'vx': 0,
                'vy': -8,
                'type': 'player'
            })
            pyxel.play(0, 0)
            
            # Create muzzle flash particles
            for _ in range(5):
                self.particles.append(Particle(
                    self.player['x'] + random.randint(-4, 4),
                    self.player['y'] - 8,
                    random.uniform(-2, 2),
                    random.uniform(-4, -1),
                    random.choice([9, 10, 11]),
                    15
                ))
    
    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet['x'] += bullet['vx']
            bullet['y'] += bullet['vy']
            
            # Remove off-screen bullets
            if bullet['y'] < -10 or bullet['y'] > 202 or bullet['x'] < -10 or bullet['x'] > 266:
                self.bullets.remove(bullet)
    
    def update_enemies(self):
        for enemy in self.enemies[:]:
            # Complex movement patterns
            if enemy['type'] == 'sine':
                enemy['y'] += enemy['speed']
                enemy['x'] += math.sin(enemy['y'] * 0.1) * 2
            elif enemy['type'] == 'spiral':
                enemy['angle'] += 0.1
                enemy['x'] += math.cos(enemy['angle']) * 2
                enemy['y'] += enemy['speed']
            else:
                enemy['y'] += enemy['speed']
                enemy['x'] += enemy.get('vx', 0)
            
            # Enemy shooting
            if random.randint(0, 120) == 0:
                self.bullets.append({
                    'x': enemy['x'],
                    'y': enemy['y'] + 8,
                    'vx': 0,
                    'vy': 3,
                    'type': 'enemy'
                })
            
            # Remove off-screen enemies
            if enemy['y'] > 200:
                self.enemies.remove(enemy)
    
    def update_powerups(self):
        for powerup in self.powerups[:]:
            powerup['y'] += 2
            powerup['angle'] += 0.2
            
            if powerup['y'] > 200:
                self.powerups.remove(powerup)
    
    def update_starfield(self):
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > 191:
                star['y'] = 0
                star['x'] = random.randint(0, 255)
    
    def spawn_enemies(self):
        """Spawn enemies based on game progression"""
        # no enemies if boss is active
        if self.boss_active:
            return
            
        # 10 enemies defeated to spawn boss
        if self.enemies_defeated >= 10 and not self.boss:
            self.spawn_boss()
            return
            
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer > max(30 - self.level * 2, 10):
            self.enemy_spawn_timer = 0
            enemy_type = random.choice(['normal', 'sine', 'spiral'])
            self.enemies.append({
                'x': random.randint(20, 236),
                'y': -10,
                'speed': random.uniform(1, 3),
                'type': enemy_type,
                'angle': 0,
                'vx': random.uniform(-1, 1) if enemy_type == 'normal' else 0
            })
    
    def spawn_boss(self):
        """Spawn the boss enemy - Initialize boss attributes and state"""
        self.boss = {
            'x': 128,
            'y': 40,
            'vx': 1,
            'health': 50,
            'max_health': 50,
            'shoot_timer': 0,
            'pattern': 0,  # 0: straight, 1: fan, 2: circle
            'phase_timer': 0
        }
        self.boss_active = True
        self.shake_intensity = 20  # Start camera shake on boss spawn
    
    def update_boss(self):
        """Update boss state - Handle movement, shooting patterns, and health management"""
        if not self.boss:
            return
            
        # Boss movement
        self.boss['x'] += self.boss['vx']
        if self.boss['x'] <= 50 or self.boss['x'] >= 206:
            self.boss['vx'] *= -1
        
        # Boss shooting timer and pattern management
        self.boss['shoot_timer'] += 1
        self.boss['phase_timer'] += 1
        
        # Change shooting pattern every 180 frames
        if self.boss['phase_timer'] > 180:
            self.boss['pattern'] = (self.boss['pattern'] + 1) % 3
            self.boss['phase_timer'] = 0
        
        # Boss shooting logic
        if self.boss['pattern'] == 0:  # basic straight shots
            if self.boss['shoot_timer'] % 8 == 0:
                for i in range(5):
                    self.bullets.append({
                        'x': self.boss['x'] - 60 + i * 30,
                        'y': self.boss['y'] + 16,
                        'vx': 0,
                        'vy': 4,
                        'type': 'enemy'
                    })
        
        elif self.boss['pattern'] == 1:  # yawning fan pattern
            if self.boss['shoot_timer'] % 12 == 0:
                for i in range(7):
                    angle = (i - 3) * 0.3
                    self.bullets.append({
                        'x': self.boss['x'],
                        'y': self.boss['y'] + 16,
                        'vx': math.sin(angle) * 3,
                        'vy': math.cos(angle) * 3 + 2,
                        'type': 'enemy'
                    })
        
        elif self.boss['pattern'] == 2:  # circle pattern
            if self.boss['shoot_timer'] % 15 == 0:
                for i in range(12):
                    angle = i * math.pi * 2 / 12
                    self.bullets.append({
                        'x': self.boss['x'],
                        'y': self.boss['y'] + 16,
                        'vx': math.cos(angle) * 2,
                        'vy': math.sin(angle) * 2 + 1,
                        'type': 'enemy'
                    })
    
    def check_collisions(self):
        # Bullet vs enemy
        for bullet in self.bullets[:]:
            if bullet['type'] == 'player':
                for enemy in self.enemies[:]:
                    if (abs(bullet['x'] - enemy['x']) < 8 and 
                        abs(bullet['y'] - enemy['y']) < 8):
                        self.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        self.score += 100
                        self.enemies_defeated += 1  # count defeated enemies 
                        self.create_explosion(enemy['x'], enemy['y'])
                        pyxel.play(1, 1)
                        
                        # Chance to spawn power-up
                        if random.randint(0, 4) == 0:
                            self.powerups.append({
                                'x': enemy['x'],
                                'y': enemy['y'],
                                'angle': 0
                            })
                        break
        
        # player bullet vs boss
        if self.boss:
            for bullet in self.bullets[:]:
                if bullet['type'] == 'player':
                    if (abs(bullet['x'] - self.boss['x']) < 32 and 
                        abs(bullet['y'] - self.boss['y']) < 16):
                        self.bullets.remove(bullet)
                        self.boss['health'] -= 1
                        self.create_explosion(bullet['x'], bullet['y'])
                        pyxel.play(1, 1)
                        
                        if self.boss['health'] <= 0:
                            self.create_explosion(self.boss['x'], self.boss['y'])
                            self.score += 1000
                            self.boss = None
                            self.boss_active = False
                            self.enemies_defeated = 0  # reset defeated count
                        break
        
        # Enemy bullet vs player
        for bullet in self.bullets[:]:
            if bullet['type'] == 'enemy':
                if (abs(bullet['x'] - self.player['x']) < 12 and 
                    abs(bullet['y'] - self.player['y']) < 12):
                    self.bullets.remove(bullet)
                    self.player['health'] -= 10
                    self.shake_intensity = 10
                    
                    if self.player['health'] <= 0:
                        self.scene = "GAMEOVER"
                        pyxel.stop()
        
        # Power-up collection
        for powerup in self.powerups[:]:
            if (abs(powerup['x'] - self.player['x']) < 12 and 
                abs(powerup['y'] - self.player['y']) < 12):
                self.powerups.remove(powerup)
                self.player['health'] = min(100, self.player['health'] + 20)
                self.score += 50
                pyxel.play(2, 2)
    
    def create_explosion(self, x, y):
        self.explosions.append({'x': x, 'y': y, 'life': 30, 'radius': 0})
        
        # Add explosion particles
        for _ in range(15):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 4)
            self.particles.append(Particle(
                x, y,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                random.choice([8, 9, 10]),
                random.randint(20, 40)
            ))
    
    def camera_shake(self):
        if self.shake_intensity > 0:
            self.camera['x'] = random.randint(-self.shake_intensity, self.shake_intensity)
            self.camera['y'] = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_intensity -= 1
        else:
            self.camera['x'] = 0
            self.camera['y'] = 0
    
    def update_gameover(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.restart_game()
    
    def restart_game(self):
        """Restart the game by resetting all game state variables"""
        # Reset game state
        self.scene = "MENU"
        self.frame = 0
        
        # Clear all game objects
        self.mouse_trails.clear()
        self.particles.clear()
        self.stars.clear()
        self.bullets.clear()
        self.enemies.clear()
        self.powerups.clear()
        self.explosions.clear()
        
        # Reset player state
        self.player = {"x": 128, "y": 150, "vx": 0, "vy": 0, "health": 100}
        self.camera = {"x": 0, "y": 0}
        
        # Reset game progression
        self.score = 0
        self.level = 1
        self.enemy_spawn_timer = 0
        self.shake_intensity = 0
        self.enemies_defeated = 0
        self.boss = None
        self.boss_active = False
        
        # Recreate starfield
        self.create_starfield()
    
    def draw(self):
        pyxel.cls(0)
        
        if self.scene == "MENU":
            self.draw_menu()
        elif self.scene == "GAME":
            self.draw_game()
        elif self.scene == "GAMEOVER":
            self.draw_gameover()
    
    def draw_menu(self):
        # Animated background
        for i in range(0, 256, 16):
            pyxel.line(i, 0, i + math.sin(self.frame * 0.1 + i * 0.1) * 20, 192, 1)
        
        # Mouse trails
        for i, (x, y) in enumerate(self.mouse_trails):
            pyxel.circb(x, y, i // 4, 13 - i // 3)
        
        pyxel.text(90, 80, "KYOPAN'S PYXEL GAMES", 7)
        pyxel.text(75, 100, "Click to start", 12)
        pyxel.text(70, 120, "Move with mouse + SPACE to shoot", 6)
    
    def draw_game(self):
        # Apply camera shake
        pyxel.camera(self.camera['x'], self.camera['y'])
        
        # Draw starfield
        for star in self.stars:
            pyxel.pset(star['x'], star['y'], star['color'])
        
        # Draw player with sprite
        pyxel.blt(self.player['x'] - 8, self.player['y'] - 8, 0, 0, 0, 16, 16, 0)
        
        # Draw engine trail
        for i in range(5):
            pyxel.pset(
                self.player['x'] + random.randint(-2, 2),
                self.player['y'] + 8 + i * 2,
                random.choice([9, 10])
            )
        
        # Draw enemies
        for enemy in self.enemies:
            pyxel.blt(enemy['x'] - 4, enemy['y'] - 4, 0, 16, 0, 8, 8, 0)
        
        # Draw boss
        if self.boss:
            pyxel.blt(self.boss['x'] - 16, self.boss['y'] - 16, 0, 32, 8, 32, 32, 0)
            
            # BOSS health bar
            bar_width = 100
            bar_x = 78
            bar_y = 10
            health_ratio = self.boss['health'] / self.boss['max_health']
            
            pyxel.rect(bar_x - 2, bar_y - 2, bar_width + 4, 8, 0)
            pyxel.rect(bar_x, bar_y, bar_width, 4, 1)
            pyxel.rect(bar_x, bar_y, int(bar_width * health_ratio), 4, 8)
            pyxel.text(bar_x, bar_y - 8, "BOSS", 7)
        
        # Draw bullets
        for bullet in self.bullets:
            color = 11 if bullet['type'] == 'player' else 8
            pyxel.rect(bullet['x'] - 1, bullet['y'] - 2, 2, 4, color)
        
        # Draw power-ups
        for powerup in self.powerups:
            pyxel.blt(powerup['x'] - 4, powerup['y'] - 4, 0, 24, 0, 8, 8, 0)
            # Rotating effect
            for i in range(4):
                angle = powerup['angle'] + i * math.pi / 2
                x = powerup['x'] + math.cos(angle) * 6
                y = powerup['y'] + math.sin(angle) * 6
                pyxel.pset(x, y, 10)
        
        # Draw explosions
        for explosion in self.explosions:
            for i in range(explosion['radius']):
                angle = random.uniform(0, math.pi * 2)
                x = explosion['x'] + math.cos(angle) * i
                y = explosion['y'] + math.sin(angle) * i
                pyxel.pset(x, y, random.choice([8, 9, 10]))
        
        # Draw particles
        for particle in self.particles:
            alpha = particle.life / particle.max_life
            if alpha > 0.5:
                pyxel.pset(particle.x, particle.y, particle.color)
        
        # Reset camera
        pyxel.camera()
        
        # Draw UI
        pyxel.rect(5, 5, 50, 6, 0)
        pyxel.rect(5, 5, int(50 * self.player['health'] / 100), 6, 8)
        pyxel.text(5, 15, f"Score: {self.score}", 7)
        pyxel.text(5, 25, f"Defeated: {self.enemies_defeated}/10", 7)
        if self.boss_active:
            pyxel.text(5, 35, "BOSS FIGHT!", 8)
        
        # Mini-map
        pyxel.rectb(200, 5, 50, 40, 7)
        for enemy in self.enemies:
            pyxel.pset(200 + enemy['x'] // 5, 5 + enemy['y'] // 5, 8)
        pyxel.pset(200 + self.player['x'] // 5, 5 + self.player['y'] // 5, 11)
    
    def draw_gameover(self):
        pyxel.cls(0)
        pyxel.text(100, 80, "GAME OVER", 8)
        pyxel.text(85, 100, f"Final Score: {self.score}", 7)
        pyxel.text(85, 120, "Press R to restart", 12)

UltimatePyxelGame()