class Coord:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def distance(self):
        return abs(self.x) + abs(self.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

class LineSegment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def horizontal(self):
        return self.start.y == self.end.y

    def intersects(self, other):
        res = False
        for (first, second) in [(self, other), (other, self)]:
            res = res or (first.start.x <= second.start.x <= first.end.x \
                          or first.end.x <= second.start.x <= first.start.x) \
                      and (second.start.y <= first.start.y <= second.end.y \
                          or second.end.y <= first.start.y <= second.start.y)
        if res:
            if self.horizontal():
                return Coord(other.start.x, self.start.y)
            else:
                return Coord(self.start.x, other.start.y)
        else:
            return False

    def __repr__(self):
        return f"{self.start}->{self.end}"

def decode(direction_string):
    direction = direction_string[0]
    num = int(direction_string[1:])
    return (direction, num)

def move(start, direction):
    dir, num = direction
    if dir == "U":
        return Coord(start.x, start.y+num)
    elif dir == "D":
        return Coord(start.x, start.y-num)
    elif dir == "L":
        return Coord(start.x-num, start.y)
    elif dir == "R":
        return Coord(start.x+num, start.y)


def get_coords(directions):
    pos = Coord()
    coords = []
    for direction in directions:
        pos = move(pos, direction)
        coords.append(pos)
    return coords


with open('input','r') as f:
    wire_1, wire_2, _ = f.read().split("\n")

wire_1 = wire_1.split(',')
wire_2 = wire_2.split(',')
wire_1 = [decode(x) for x in wire_1]
wire_2 = [decode(x) for x in wire_2]

coords1 = get_coords(wire_1)
coords2 = get_coords(wire_2)

intersections = []
for i in range(0, len(coords2)-1):
    l2 = LineSegment(coords2[i], coords2[i+1])
    for j in range(0, len(coords1)-1):
        l1 = LineSegment(coords1[j], coords1[j+1])
        intersection = l1.intersects(l2)
        if intersection:
            intersections.append(intersection)

print(min([x.distance() for x in intersections]))
