import pyxel

# Initialize a 200×200 window
pyxel.init(200, 200)

# Ball’s initial state
ballx = 100
bally = 0
vx = 0.866  # cos(30°)
vy = 0.5    # sin(30°)
speed = 3.0

# Paddle’s dimensions
pad_width = 40
pad_height = 5
pad_x = (pyxel.width - pad_width) // 2
pad_y = pyxel.height - 10  # 10px above bottom

# Score
score = 0

def update():
    global ballx, bally, vx, speed, score, pad_x

    # --- Paddle follows the mouse's X position ---
    pad_x = pyxel.mouse_x - pad_width // 2
    # Clamp pad_x so it stays fully on screen
    pad_x = max(0, min(pad_x, pyxel.width - pad_width))

    # --- Ball movement ---
    ballx += vx * speed
    bally += vy * speed

    # Bounce off left/right edges
    if ballx <= 0 or ballx >= pyxel.width:
        vx = -vx

    # When the ball reaches the bottom edge
    if bally >= pyxel.height:
        # Check if it hits the paddle
        if pad_x <= ballx <= pad_x + pad_width and bally >= pad_y:
            score += 1  # Successful catch → increment score
        # Reset ball to top
        ballx = 100
        bally = 0
        speed += 0.1  # Increase speed slightly each round

def draw():
    # Clear the screen with color 7 (gray)
    pyxel.cls(7)
    # Draw the ball
    pyxel.circ(ballx, bally, 10, 6)
    # Draw the paddle
    pyxel.rect(pad_x, pad_y, pad_width, pad_height, 11)
    # Draw the score at top-left
    pyxel.text(5, 5, f"Score: {score}", 0)

# Start the Pyxel application
pyxel.run(update, draw)