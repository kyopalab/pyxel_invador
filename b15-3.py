from collections import deque, namedtuple
import pyxel

Point = namedtuple("Point", ["x", "y"])

class Snake:

    def __init__(self):
        pyxel.init(40, 50, fps=5)
        self.direction = Point(1, 0)
        self.snake = deque()
        self.snake.append(Point(5, 5))
        pyxel.run(self.update, self.draw)

    def update(self):
        head = self.snake[0]
        self.snake.appendleft(Point(head.x + self.direction.x,
                                    head.y + self.direction.y))

    def draw(self):
        pyxel.cls(3)
        for x, y in self.snake:
            pyxel.pset(x, y, 7)

Snake()