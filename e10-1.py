import pyxel

# Initialize a 200×200 window
pyxel.init(200, 200)
pyxel.mouse(True)

# Game parameters
ball_count = 3
speed = 1.0
score = 0

# Paddle dimensions
pad_width = 40
pad_height = 5
pad_y = pyxel.height - 10  # 10 px above bottom
pad_x = (pyxel.width - pad_width) // 2

# Lists to hold each ball’s state
ballxs = [0] * ball_count
ballys = [0] * ball_count
vxs = [0] * ball_count
vys = [0] * ball_count

def reset_ball(i):
    """Place ball i at a random x along the top with a random angle 30°–150°."""
    ballxs[i] = pyxel.rndi(0, pyxel.width - 1)
    ballys[i] = 0
    angle = pyxel.rndi(30, 150)
    vxs[i] = pyxel.cos(angle)
    vys[i] = pyxel.sin(angle)

# Initialize all balls
for i in range(ball_count):
    reset_ball(i)

def update():
    global pad_x, speed, score

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
            # Check catch
            if pad_x <= ballxs[i] <= pad_x + pad_width:
                score += 1
            # Speed up next round
            speed += 0.1
            # Reset this ball
            reset_ball(i)

def draw():
    # Clear screen
    pyxel.cls(7)
    # Draw balls
    for i in range(ball_count):
        pyxel.circ(ballxs[i], ballys[i], 10, 6)
    # Draw paddle
    pyxel.rect(pad_x, pad_y, pad_width, pad_height, 11)
    # Draw score
    pyxel.text(5, 5, f"Score: {score}", 0)

# Start the game loop
pyxel.run(update, draw)