import pyxel

# Window size
WIDTH = 200
HEIGHT = 200

# Length of each diagonal segment
SEGMENT_LENGTH = 100

# Frame counter (will run from 0 to SEGMENT_LENGTH and then reset)
frame = 0

def update():
    global frame
    # Advance the frame counter
    frame += 1
    # When we complete one diagonal, start over
    if frame > SEGMENT_LENGTH:
        frame = 0

def draw():
    global frame
    pyxel.cls(7)  # clear screen to light gray
    
    t = frame
    
    # Circle 1: moves from (100, 0) → (200, 100)
    x1 = 100 + t
    y1 = 0   + t
    pyxel.circ(x1, y1, 10, 0)  # radius=10, color index=0 (black)
    
    # Circle 2: moves from (200, 100) → (100, 200)
    x2 = 200 - t
    y2 = 100 + t
    pyxel.circ(x2, y2, 10, 0)  # color index=8 (dark blue)
    
    # Circle 3: moves from (100, 200) → (0, 100)
    x3 = 100 - t
    y3 = 200 - t
    pyxel.circ(x3, y3, 10, 0) # color index=11 (red)
    
    # Circle 4: moves from (0, 100) → (100, 0)
    x4 = 0   + t
    y4 = 100 - t
    pyxel.circ(x4, y4, 10, 0)  # color index=3 (green)

# Initialize Pyxel and start the loop
pyxel.init(WIDTH, HEIGHT)
pyxel.run(update, draw)