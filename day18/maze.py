import math
from heapq import *

with open('input') as f:
    input = f.read()[:-1]

class State:
    def __init__(self, maze, pos, keys=set()):
        self.pos = frozenset(pos)
        self.keys = frozenset(keys)
        self.maze = maze
        self.cost = math.inf

    @property
    def dist(self):
        return self.cost + self.h()

    def h(self):
        """ heuristic """
        total_keys = len(self.maze.keys.keys())
        key_diff = total_keys - len(self.keys)
        return key_diff

    @property
    def neighbours(self):
        neighbours = []
        for x, y in self.pos:
            for neighbour in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                char = self.maze[neighbour]
                keys = set(self.keys)
                if char != '#':
                    if 'a' <= char <= 'z':
                        keys.add(char)
                    if 'A' <= char <= 'Z':
                        if char.lower() not in keys:
                            # cannot open
                            continue
                    pos = set(self.pos)
                    pos.remove((x,y))
                    pos.add(neighbour)
                    neighbour = State(self.maze, pos, keys)
                    neighbour.cost = self.cost + 1
                    neighbours.append(neighbour)
        return neighbours

    def __eq__(self, other):
        return (self.pos == other.pos and
                self.keys == other.keys)

    def __lt__(self, other):
        return self.dist < other.dist

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

    def draw(self):
        dim_x, dim_y = self.shape
        string = ""
        for y in range(dim_y):
            for x in range(dim_x):
                string += self.maze[(x,y)]
            string += '\n'
        return string

    def solution(self):
        unvisited = []
        visited = set()
        current = State(self, self.pos)
        current.cost = 0
        all_keys = len(self.keys.keys())
        max_keys = 0
        while True:
            # print(current)
            if len(current.keys) == all_keys:
                return current.cost
            if len(current.keys) > max_keys:
                max_keys = len(current.keys)
                # print(current.keys)
            for neighbour in current.neighbours:
                if neighbour not in visited:
                    heappush(unvisited, neighbour)
            visited.add(current)
            current = heappop(unvisited)

    def split(self):
        x, y = self.pos.pop()
        for location in [(x-1,y-1), (x-1,y+1), (x+1, y-1), (x+1, y+1)]:
            self.maze[location] = '@'
            self.pos.add(location)
        for diff in range(-1,2):
            self.maze[(x+diff, y)] = '#'
            self.maze[(x, y+diff)] = '#'

maze = Maze(input)
print("1. {}".format(maze.solution()))
