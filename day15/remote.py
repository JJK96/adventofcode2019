import intcode
import math
import pickle

class Node:
    def __init__(self, pos):
        self.pos = pos
        self.dist = math.inf

class Droid:
    def __init__(self, program, do_print=False):
        self.do_print = do_print
        self.pos = (0, 0)
        # empty places that the droid can move to
        self.map = {}
        self.map[self.pos] = '.'
        self.empty_places = set()
        self.update_empty_places()
        self.steps = []
        self.dest = None
        self.computer = intcode.Computer(program, self.get_input, output_callback=self.output_handler)
        self.computer.run()

    def get_new_pos(self, direction, start=None):
        if not start:
            start = self.pos
        x, y = start
        if direction == 1:
            return (x, y-1)
        elif direction == 2:
            return (x, y+1)
        elif direction == 3:
            return (x-1, y)
        elif direction == 4:
            return (x+1, y)

    def empty(self, x):
        item = self.map.get(x)
        return item == '.' or item == '!'

    def draw_map(self):
        x_range = [0,0]
        y_range = [0,0]
        for k in self.map.keys():
            x, y = k
            if x < x_range[0]:
                x_range[0] = x
            if x > x_range[1]:
                x_range[1] = x
            if y < y_range[0]:
                y_range[0] = y
            if y > y_range[1]:
                y_range[1] = y
        map = [[" " for _ in range(x_range[0], x_range[1]+1)] for _ in range(y_range[0], y_range[1]+1 )]
        for k, v in self.map.items():
            x, y = k
            x -= x_range[0]
            y -= y_range[0]
            map[y][x] = v
        string = ""
        for line in map:
            for char in line:
                string += char
            string += "\n"
        return string

    def get_steps(self, dest, start=None):
        if not start:
            start = self.pos
        unvisited = {x:Node(x) for x in self.map.keys() if self.empty(x)}
        unvisited[dest] = Node(dest)
        current = unvisited[start]
        current.dist = 0
        current.path = []
        while True:
            for direction in range(1, 5):
                new_pos = self.get_new_pos(direction, current.pos)
                neighbour = unvisited.get(new_pos)
                if not neighbour:
                    continue
                new_dist = current.dist+1
                if neighbour.dist > new_dist:
                    neighbour.dist = new_dist
                    neighbour.path = current.path + [direction]
                if neighbour.pos == dest:
                    return neighbour.path
            del unvisited[current.pos]
            if len(unvisited.keys()) > 0:
                current = min(unvisited.values(), key=lambda node: node.dist)
            else:
                break
        print("no path found")
        return []

    def update_empty_places(self):
        for direction in range(1, 5):
            new_pos = self.get_new_pos(direction)
            item = self.map.get(new_pos, ' ')
            if item == ' ':
                self.empty_places.add(new_pos)

    def get_input(self):
        try:
            if not self.dest:
                self.dest = next(iter(self.empty_places))
                steps = self.get_steps(self.dest)
                self.steps = steps
            return self.steps[0]
        except:
            # done
            pass

    def output_to_char(self, output):
        if output == 0:
            return '█'
        elif output == 1:
            return '.'
        elif output == 2:
            return '!'

    def output_handler(self, output):
        new_pos = self.get_new_pos(self.steps[0])
        self.steps = self.steps[1:]
        if new_pos == self.dest:
            self.empty_places.remove(new_pos)
            self.dest = None
            if self.do_print:
                print(self.draw_map())
        output = self.output_to_char(output)
        self.map[new_pos] = output
        if output != '█':
            self.pos = new_pos
            if output == '!':
                self.oxygen_system = new_pos
            self.update_empty_places()

    def spread_oxygen(self):
        time = 0
        self.map[self.oxygen_system] = 'O'
        filled = False
        while not filled:
            time += 1
            filled = True
            for k, v in list(self.map.items()):
                if v == 'O':
                    for direction in range(1,5):
                        new_pos = self.get_new_pos(direction, k)
                        item = self.map.get(new_pos)
                        if item == '.':
                            self.map[new_pos] = 'O'
                elif v == '.':
                    filled = False
        return time-1

with open('input') as f:
    program = intcode.convert(f.read())

droid = Droid(program, do_print=False)
steps = droid.get_steps(droid.oxygen_system, (0,0))
print("1. " + str(len(steps)))
print("2. " + str(droid.spread_oxygen()))
