import pyxel

# Initialize a 200×200 window
pyxel.init(200, 200)

# Set the ball’s initial position to (100, 0)
ballx = 100
bally = 0

# Base direction vector at 30° from the horizontal
vx = 0.866  # cos(30°)
vy = 0.5    # sin(30°)

# Speed multiplier (1.0 = original speed)
speed = 10.0

def update():
    global ballx, bally, vx, speed

    # Move the ball by its direction vector scaled by speed
    ballx += vx * speed
    bally += vy * speed

    # Bounce off the left and right edges by reversing vx
    if ballx <= 0 or ballx >= pyxel.width:
        vx = -vx

    # When the ball passes the bottom edge:
    if bally >= pyxel.height:
        # Reset to the starting position
        ballx = 100
        bally = 0
        # Increase speed slightly for the next run
        speed += 0.1

def draw():
    # Clear the screen with color 7 (gray)
    pyxel.cls(7)
    # Draw the ball as a circle with radius 10 and color 6
    pyxel.circ(ballx, bally, 10, 6)

# Start the Pyxel application, calling update() and draw() each frame
pyxel.run(update, draw)