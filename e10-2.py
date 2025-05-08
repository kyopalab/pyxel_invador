import pyxel

# Initialize a 200×200 window
pyxel.init(200, 200)
pyxel.mouse(True)

# Game parameters
ball_count = 3
speed = 1.0
score = 0
misses = 0
game_over = False  # tracks whether the game has ended

# Paddle dimensions and position
pad_width = 40
pad_height = 5
pad_y = pyxel.height - 10
pad_x = (pyxel.width - pad_width) // 2

# Lists to hold each ball’s state
ballxs = [0] * ball_count
ballys = [0] * ball_count
vxs = [0] * ball_count
vys = [0] * ball_count

def reset_ball(i):
    """Place ball i at random x along the top with a random angle 30°–150°."""
    ballxs[i] = pyxel.rndi(0, pyxel.width - 1)
    ballys[i] = 0
    angle = pyxel.rndi(30, 150)
    vxs[i] = pyxel.cos(angle)
    vys[i] = pyxel.sin(angle)

# Initialize all balls
for i in range(ball_count):
    reset_ball(i)

def update():
    global pad_x, speed, score, misses, game_over

    # If the game is over, do nothing
    if game_over:
        return

    # Paddle follows mouse X
    pad_x = pyxel.mouse_x - pad_width // 2
    pad_x = max(0, min(pad_x, pyxel.width - pad_width))

    # Update each ball
    for i in range(ball_count):
        ballxs[i] += vxs[i] * speed
        ballys[i] += vys[i] * speed

        # Bounce off left/right edges
        if ballxs[i] <= 0 or ballxs[i] >= pyxel.width:
            vxs[i] = -vxs[i]

        # When ball reaches bottom
        if ballys[i] >= pyxel.height:
            # Check for catch
            if pad_x <= ballxs[i] <= pad_x + pad_width:
                score += 1
            else:
                misses += 1
                # If 10 misses accumulate, end the game
                if misses >= 10:
                    game_over = True
            speed += 0.1  # speed up next round
            reset_ball(i)

def draw():
    # If the game is over, just display "Game Over" on top of the current frame
    if game_over:
        pyxel.text(80, 90, "GAME OVER", 8)
        pyxel.text(70, 110, f"Final Score: {score}", 7)
        return

    # Otherwise, clear and draw the current game state
    pyxel.cls(7)
    # Draw balls
    for i in range(ball_count):
        pyxel.circ(ballxs[i], ballys[i], 10, 6)
    # Draw paddle
    pyxel.rect(pad_x, pad_y, pad_width, pad_height, 11)
    # Draw score and misses
    pyxel.text(5, 5, f"Score: {score}", 0)
    pyxel.text(5, 15, f"Misses: {misses}", 0)

# Start the game loop
pyxel.run(update, draw)