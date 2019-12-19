import math
from heapq import *
from copy import copy
from collections import deque

with open('input') as f:
    input = f.read()[:-1]

# input = """#################
# #i.G..c...e..H.p#
# ########.########
# #j.A..b...f..D.o#
# ########@########
# #k.E..a...g..B.n#
# ########.########
# #l.F..d...h..C.m#
# #################"""

# input="""########################
# #...............b.C.D.f#
# #.######################
# #.....@.a.B.c.d.A.e.F.g#
# ########################"""

# input = """#############
# #g#f.D#..h#l#
# #F###e#E###.#
# #dCba@#@BcIJ#
# #############
# #nK.L@#@G...#
# #M###N#H###.#
# #o#m..#i#jk.#
# #############"""

class State:
    def __init__(self, maze, pos):
        self.pos = pos
        self.maze = maze
        self.cost = math.inf

    @property
    def neighbours(self):
        neighbours = []
        x, y = self.pos
        for neighbour in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            char = self.maze[neighbour]
            if char != '#':
                neighbour = State(self.maze, neighbour)
                neighbour.cost = self.cost + 1
                neighbours.append(neighbour)
        return neighbours

    def __eq__(self, other):
        return (self.pos == other.pos)

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        return hash(self.pos)

class KeyState:
    def __init__(self, maze, pos, keys=set(), path=[]):
        self.pos = frozenset(pos)
        self.maze = maze
        self.cost = math.inf
        self.keys = frozenset(keys)
        self.path = path

    @property
    def dist(self):
        return self.cost

    def h(self):
        """ heuristic """
        total_keys = len(self.maze.keys.keys())
        key_diff = total_keys - len(self.keys)
        return key_diff

    @property
    def neighbours(self):
        neighbours = []
        for pos in self.pos:
            for neighbour, cost in self.maze.distance_map[pos].items():
                keys = set(self.keys)
                path = copy(self.path)
                path.append(self)
                char = self.maze[neighbour]
                if 'a' <= char <= 'z':
                    keys.add(char)
                if 'A' <= char <= 'Z' and char.lower() not in keys:
                    # cannot open
                    continue
                new_pos = set(self.pos)
                new_pos.remove(pos)
                new_pos.add(neighbour)
                neighbour = KeyState(self.maze, new_pos, keys, path)
                neighbour.cost = self.cost + cost
                if neighbour != self:
                    neighbours.append(neighbour)
        return neighbours

    def __lt__(self, other):
        return self.dist < other.dist

    def __eq__(self, other):
        return (self.pos == other.pos and self.keys == other.keys)

    def positions_str(self):
        positions = []
        for x, y in sorted(self.pos):
            positions.append(f"({x}, {y})")
        return ','.join(positions)

    def __str__(self):
        string = "[{}] keys={}, cost={}".format(self.positions_str(), self.keys, self.cost)
        return string

    def __hash__(self):
        return hash(self.positions_str()) ^ hash(self.keys)


class Maze:
    def __init__(self, input=None):
        self.shape = None
        self.maze = {}
        self.keys = {}
        self.doors = {}
        self.pos = set()
        if input:
            self.init_maze(input)
        self.distance_map = {}

    def __getitem__(self, item):
        return self.maze[item]

    def init_maze(self, input):
        lines = input.split('\n')
        dim_y = len(lines)
        for y, line in enumerate(lines):
            dim_x = len(line)
            for x, char in enumerate(line):
                self.maze[(x, y)] = char
                if char == '@':
                    self.pos.add((x, y))
                elif 'a' <= char <= 'z':
                    self.keys[char] = (x,y)
                elif 'A' <= char <= 'Z':
                    self.doors[char] = (x,y)
        self.shape = (dim_x, dim_y)

    def draw(self, positions=None):
        dim_x, dim_y = self.shape
        string = ""
        for y in range(dim_y):
            for x in range(dim_x):
                char = self.maze[(x,y)]
                if char == '#':
                    char = '█'
                if positions is not None:
                    if (x,y) in positions:
                        char = '@'
                    else:
                        if char == '@':
                            char = '.'
                string += char
            string += '\n'
        return string

    def solution(self):
        unvisited = []
        current = KeyState(self, self.pos)
        current.cost = 0
        states = {}
        all_keys = len(self.keys.keys())
        max_keys = 0
        while True:
            # print(current)
            if len(current.keys) == all_keys:
                return current.path, current.cost
            if len(current.keys) > max_keys:
                max_keys = len(current.keys)
                print(current.keys)
            for neighbour in current.neighbours:
                neighbour_best = states.get(neighbour)
                if neighbour_best is None or neighbour.cost < neighbour_best.cost:
                    states[neighbour] = neighbour
                    if neighbour not in unvisited:
                        heappush(unvisited, neighbour)
            current = heappop(unvisited)

    def distances(self):
        """ calculate distances between keys and the entrance """
        positions = set(self.keys.values())
        positions.update(self.pos)
        positions.update(self.doors.values())
        self.distance_map = {}
        for position in positions:
            distances_others = {}
            unvisited = []
            states = {}
            start = State(self, position)
            start.cost = 0
            unvisited.append(start)
            while len(unvisited) > 0:
                current = heappop(unvisited)
                if current.pos in positions:
                    if current.pos not in distances_others.keys() and current.pos != position:
                        distances_others[current.pos] = current.cost
                        continue
                for neighbour in current.neighbours:
                    neighbour_best = states.get(neighbour)
                    if neighbour_best is None or neighbour.cost < neighbour_best.cost:
                        states[neighbour] = neighbour
                        heappush(unvisited, neighbour)
            self.distance_map[position] = distances_others

    def split(self):
        x, y = self.pos.pop()
        for location in [(x-1,y-1), (x-1,y+1), (x+1, y-1), (x+1, y+1)]:
            self.maze[location] = '@'
            self.pos.add(location)
        for diff in range(-1,2):
            self.maze[(x+diff, y)] = '#'
            self.maze[(x, y+diff)] = '#'

maze = Maze(input)
# print("1. {}".format(maze.solution()))
maze.distances()
print(maze.distance_map)
# for k, v in maze.distance_map.items():
#     print(maze[k])
#     for k, v in v.items():
#         print('\t', maze[k], v)
# print(maze.draw())
# maze.split()
maze.distances()
path, cost = maze.solution()
print(cost)
