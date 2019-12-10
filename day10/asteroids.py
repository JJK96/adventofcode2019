import math

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lines = {}

    def get_key(self, other):
        diffx = (other.x - self.x)
        if diffx == 0:
            slope = math.inf
        else:
            slope = (self.y - other.y)/diffx
        up_or_right = (other.x == self.x and other.y < self.y) or other.x > self.x
        return (up_or_right, slope)

    def insert(self, other):
        key = self.get_key(other)
        on_line = self.lines.get(key, [])
        on_line.append(other)
        self.lines[key] = on_line

    def draw_map(self, width, height):
        map = [['.' for _ in range(width)] for _ in range(height)]
        map[self.y][self.x] = '#'
        for num, asteroids in enumerate(self.lines.values()):
            char = chr(num+65)
            for asteroid in asteroids:
                map[asteroid.y][asteroid.x] = char
        string = ""
        for line in map:
            for char in line:
                string += char
            string += "\n"
        return string

    def dist(self, other):
        return math.sqrt((self.x-other.y)**2 + (self.y - other.y)**2)

    def laser(self):
        sorted_keys = sorted(self.lines.keys(), reverse=True)
        obliterated = []
        did_obliterate = True
        while did_obliterate:
            did_obliterate = False
            for key in sorted_keys:
                asteroids = sorted(self.lines.get(key), key=lambda x: self.dist(x))
                if len(asteroids) > 0:
                    obliterated.append(asteroids[0])
                    self.lines[key] = asteroids[1:]
                    did_obliterate = True
        return obliterated

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"({self.x}, {self.y})"

with open('input','r') as f:
    input = f.read()

asteroids = []
lines = input.split()
height = len(lines)
for y, line in enumerate(lines):
    width = len(line)
    for x, char in enumerate(line):
        if char == '#':
            asteroids.append(Asteroid(x,y))

max_lines = 0
max_asteroid = None
for asteroid in asteroids:
    for other in asteroids:
        if asteroid != other:
            asteroid.insert(other)
    num_lines = len(asteroid.lines.keys())
    if num_lines > max_lines:
        max_lines = num_lines
        max_asteroid = asteroid
print(f"1. {max_lines}")
obliterated = max_asteroid.laser()
x200th = obliterated[200-1]
print(f"2. {x200th.x*100 + x200th.y}")
