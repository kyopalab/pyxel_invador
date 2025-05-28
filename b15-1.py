from collections import namedtuple

foo = namedtuple("Point", ["x", "y"])

p = foo(1, 2)
print(p)    # displays "Point(x=1, y=2)"

# retrieve values by name
print(p.x)
print(p.y)

# retrieve values by decomposition
(a, b) = p
print(a)
print(b)