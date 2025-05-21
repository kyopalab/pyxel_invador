import pyxel

class Ball:
    """A single falling ball with its own position and velocity."""
    def __init__(self):
        self.restart()

    def restart(self):
        """Initialize at random top-side X and random angle (30°–150°)."""
        self.x  = pyxel.rndi(0, pyxel.width - 1)
        self.y  = 0
        angle   = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)

    def move(self, speed):
        """
        Move the ball; bounce off left/right.
        If it reaches bottom, restart and return True.
        """
        self.x += self.vx * speed
        self.y += self.vy * speed

        # bounce horizontally
        if self.x <= 0 or self.x >= pyxel.width:
            self.vx = -self.vx

        # reached bottom?
        if self.y >= pyxel.height:
            self.restart()
            return True
        return False

    def update(self, speed):
        """Advance the ball and return whether it hit the bottom."""
        return self.move(speed)

    def draw(self):
        """Draw the ball as a 10px circle."""
        pyxel.circ(self.x, self.y, 10, 6)


class Pad:
    """Mouse-controlled paddle."""
    def __init__(self):
        self.width  = 40
        self.height = 5
        self.y      = pyxel.height - 10
        self.x      = (pyxel.width - self.width) // 2

    def update(self):
        """Follow the mouse's X, clamped to screen."""
        self.x = pyxel.mouse_x - self.width // 2
        self.x = max(0, min(self.x, pyxel.width - self.width))

    def draw(self):
        """Draw the paddle as a rectangle."""
        pyxel.rect(self.x, self.y, self.width, self.height, 11)

    def catch(self, ball):
        """
        Return True if ball is caught by paddle bounds, else False.
        """
        return self.x <= ball.x <= self.x + self.width


class App:
    """Encapsulates game state; no globals used."""
    def __init__(self):
        pyxel.init(200, 200, fps=30)
        pyxel.mouse(True)

        # game state
        self.initial_speed       = 1.0
        self.speed               = self.initial_speed
        self.score               = 0
        self.misses              = 0
        self.game_over           = False
        self.next_level_up_score = 10

        # objects
        self.balls = [Ball()]
        self.pad   = Pad()

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over:
            return

        # move paddle
        self.pad.update()

        # move and handle each ball
        for ball in self.balls:
            if ball.update(self.speed):
                # bottom collision → check catch
                if self.pad.catch(ball):
                    self.score += 1
                    # level up?
                    if self.score >= self.next_level_up_score:
                        self.balls.append(Ball())
                        self.speed = self.initial_speed
                        self.next_level_up_score += 10
                else:
                    self.misses += 1
                    if self.misses >= 10:
                        self.game_over = True

                # speed up next launch
                self.speed += 0.1

    def draw(self):
        if self.game_over:
            pyxel.cls(7)
            pyxel.text(80,  90, "GAME OVER",    8)
            pyxel.text(70, 110, f"Final Score: {self.score}", 7)
            return

        pyxel.cls(7)
        # draw balls and paddle
        for ball in self.balls:
            ball.draw()
        self.pad.draw()

        # HUD
        pyxel.text(5,  5, f"Score:  {self.score}",  0)
        pyxel.text(5, 15, f"Misses: {self.misses}", 0)


# start the application
App()