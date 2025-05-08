import pyxel

# Initialize a Pyxel window with dimensions 200x200 pixels
def setup():
    pyxel.init(200, 200)

# Initial ball position (x, y)
ballx = 0
bally = 0
# Velocity components: vx is the x-velocity, vy is the y-velocity
# Using values for a 60° angle: cos(60°)=0.5, sin(60°)=0.866
vx = 0.5
vy = 0.866

# Update function: moves the ball each frame
# Resets the position when the ball goes beyond the bottom boundary
def update():
    global ballx, bally, vx, vy
    # Update position by adding velocity
    ballx += vx
    bally += vy
    # If the ball moves beyond the bottom edge, reset to (0, 0)
    if bally >= 200:
        ballx = 0
        bally = 0

# Draw function: clears the screen and draws the ball
def draw():
    global ballx, bally
    # Clear the screen with color index 7 (light grey)
    pyxel.cls(7)
    # Draw a filled circle at (ballx, bally) with radius 10 and color index 6 (orange)
    pyxel.circ(ballx, bally, 10, 6)

# Start the game loop, calling update() and draw() each frame
pyxel.run(update, draw)
