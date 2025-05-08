import pyxel

# Initialize a 200×200 window and set 30 FPS
pyxel.init(200, 200, fps=30)

# Sound effect setup using pyxel.sounds[index].set(...)
# Sound 0: higher-pitched beep for successful catch
pyxel.sounds[0].set(
    notes="C4E4",   # two notes: C4 and E4
    tones="TT",     # triangle wave on both tracks
    volumes="33",   # volume level for each track
    effects="NN",   # no effects
    speed=15        # playback speed
)
# Sound 1: lower-pitched beep for miss
pyxel.sounds[1].set(
    notes="C3E3",   # two notes: C3 and E3
    tones="TT",
    volumes="33",
    effects="NN",
    speed=10
)

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
    ballx = pyxel.rndi(0, pyxel.width - 1)
    bally = 0
    angle = pyxel.rndi(30, 150)
    vx = pyxel.cos(angle)
    vy = pyxel.sin(angle)

# Initialize the first ball
reset_ball()

def update():
    global ballx, bally, vx, vy, speed, score, pad_x

    # Paddle follows the mouse's X position
    pad_x = pyxel.mouse_x - pad_width // 2
    pad_x = max(0, min(pad_x, pyxel.width - pad_width))

    # Move the ball by its velocity scaled by speed
    ballx += vx * speed
    bally += vy * speed

    # Bounce off the left and right edges
    if ballx <= 0 or ballx >= pyxel.width:
        vx = -vx

    # When the ball reaches the bottom edge
    if bally >= pyxel.height:
        # Play catch or miss sound
        if pad_x <= ballx <= pad_x + pad_width:
            score += 1
            pyxel.play(0, 0)  # channel 0, sound 0
        else:
            pyxel.play(0, 1)  # channel 0, sound 1
        speed += 0.1  # speed up next round
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