import pyxel

# Initialize a 200×200 window
pyxel.init(200, 200)

# Game state variables
ballx = 0
bally = 0
vx = 0
vy = 0
speed = 10.0
score = 0

# Paddle dimensions and position
pad_width = 40
pad_height = 5
pad_x = (pyxel.width - pad_width) // 2
pad_y = pyxel.height - 10  # 10 px above the bottom

def reset_ball():
    """Place the ball at a random x along the top and give it a random angle between 30° and 150°."""
    global ballx, bally, vx, vy
    # Randomize starting X between 0 and 199
    ballx = pyxel.rndi(0, pyxel.width - 1)
    bally = 0
    # Randomize launch angle between 30° and 150°
    angle = pyxel.rndi(30, 150)
    # Compute direction vector from angle
    vx = pyxel.cos(angle)
    vy = pyxel.sin(angle)

# Initialize the first ball
reset_ball()

def update():
    global ballx, bally, vx, vy, speed, score, pad_x

    # Paddle follows the mouse's X position
    pad_x = pyxel.mouse_x - pad_width // 2
    pad_x = max(0, min(pad_x, pyxel.width - pad_width))

    # Move the ball by its velocity vector scaled by speed
    ballx += vx * speed
    bally += vy * speed

    # Bounce off the left and right edges
    if ballx <= 0 or ballx >= pyxel.width:
        vx = -vx

    # When the ball reaches the bottom edge
    if bally >= pyxel.height:
        # Increase score if caught by the paddle
        if pad_x <= ballx <= pad_x + pad_width and bally >= pad_y:
            score += 1
        # Speed up next launch
        speed += 0.1
        # Reset ball for next round
        reset_ball()

def draw():
    # Clear the screen with color 7 (light gray)
    pyxel.cls(7)
    # Draw the ball as a circle (radius 10, color 6)
    pyxel.circ(ballx, bally, 10, 6)
    # Draw the paddle as a rectangle (color 11)
    pyxel.rect(pad_x, pad_y, pad_width, pad_height, 11)
    # Draw the score at top-left
    pyxel.text(5, 5, f"Score: {score}", 0)

# Start the Pyxel application
pyxel.run(update, draw)