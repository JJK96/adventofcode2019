from intcode import Computer, convert
from collections import defaultdict
from copy import copy

with open('input') as f:
    input_string = f.read()

program = convert(input_string)

def remove_substring(route, substring, substring_name):
    new_route = []
    previous = 0
    i = 0
    while i < len(route):
        route_part = route[i:i+len(substring)]
        if route_part == substring:
            new_route.append(substring_name)
            i += len(substring)
        else:
            new_route.append(route[i])
            i += 1
    return new_route

def split_route(route, substrings={}, route_names = ['A', 'B' ,'C']):
    if route == []:
        return substrings, route
    # print(substrings, route)
    for i in range(min(len(route), 10), 0, -1):
        substring = route[:i]
        # print(substring)
        for name, substring1 in substrings.items():
            if substring == substring1:
                res = split_route(route[i:], substrings, route_names)
                if res is not None:
                    substrings, left = res
                    return substrings, [name] + left
        if len(route_names) > 0:
            new_substrings = copy(substrings)
            new_substrings[route_names[0]] = substring
            res = split_route(route, new_substrings, route_names[1:])
            if res is not None:
                return res
    return None

def split_counts(route):
    new_route = []
    split_by = 8
    for x in route:
        if type(x) == int:
            new_route += [split_by]*(x//split_by)
            if x % split_by != 0:
                new_route.append(x % split_by)
        else:
            new_route.append(x)
    return new_route

class Vacuum:
    def __init__(self, program, video=True):
        self.scaffolding = []
        self.line = []
        self.printing = False
        self.program = program
        self.directions = ['<', 'V', '>', '^']
        self.input_state = 0
        self.inputs = []
        self.video = video
        self.route = None

    def turn(self, direction, current_direction):
        return (direction + current_direction) % len(self.directions)

    def move(self, x, y, direction):
        if direction == 0:
            return (x-1,y)
        elif direction == 1:
            return (x, y+1)
        elif direction == 2:
            return (x+1, y)
        else:
            return (x, y-1)

    def get_scaffolding(self):
        program[0] = 1
        computer = Computer(self.program, None, output_callback=self.handle_output)
        computer.run()

    def find_robots(self):
        program[0] = 2
        computer = Computer(self.program, self.get_input, output_callback=self.handle_output1)
        computer.run()

    def list_to_input(self, l):
        string = ','.join([str(x) for x in l])
        # print(f"{string=}, {len(string)=}")
        string += '\n'
        return [ord(x) for x in string]

    def get_input(self):
        if len(self.inputs) == 0:
            if self.route is None:
                self.get_route()
            if self.input_state == 0:
                # main program
                self.inputs = self.list_to_input(self.route[1])
            elif self.input_state == 1:
                self.inputs = self.list_to_input(self.route[0]['A'])
            elif self.input_state == 2:
                self.inputs = self.list_to_input(self.route[0]['B'])
            elif self.input_state == 3:
                self.inputs = self.list_to_input(self.route[0]['C'])
            elif self.input_state == 4:
                if self.video:
                    string = "y"
                else:
                    string = "n"
                string += "\n"
                self.inputs = [ord(x) for x in string]
            self.input_state += 1
        res = self.inputs[0]
        self.inputs = self.inputs[1:]
        return res

    def handle_output1(self, output):
        if output > 127:
            self.dust = output
            if self.video:
                print(self.dust)
        else:
            if self.video:
                print(chr(output), end='')

    def handle_output(self, output):
        if not self.printing:
            self.scaffolding = []
            self.printing = True
        char = chr(output)
        if char == '\n':
            if self.line:
                self.scaffolding.append(self.line)
            else:
                self.printing = False
            self.line = []
        else:
            if self.is_vacuum(char):
                x = len(self.line)
                y = len(self.scaffolding)
                self.vacuum = (x, y)
            self.line.append(char)

    def print_scaffolding(self):
        for line in self.scaffolding:
            print(''.join(line))

    def is_scaffolding(self, x, y):
        if x < 0 or y < 0:
            return False
        try:
            char = self.scaffolding[y][x]
            return char != '.'
        except IndexError:
            return False

    def is_vacuum(self, char):
        try:
            direction = self.directions.index(char)
            self.direction = direction
            return True
        except ValueError:
            return False

    def turn_to_char(self, turn):
        if turn == 1:
            return 'L'
        elif turn == 0:
            return 'N'
        else:
            return 'R'

    def get_route(self):
        x, y = self.vacuum
        # print(f"{x=}, {y=}")
        direction = self.direction
        route = []
        found_scaffolding = True
        while found_scaffolding:
            for turn in [0, 1, -1]:
                new_direction = self.turn(turn, direction)
                next_x, next_y = self.move(x, y, new_direction)
                found_scaffolding = self.is_scaffolding(next_x, next_y)
                if found_scaffolding:
                    turn = self.turn_to_char(turn)
                    # print(f"{next_x=}, {next_y=}, {new_direction=}, {turn=}")
                    route.append(turn)
                    x = next_x
                    y = next_y
                    direction = new_direction
                    break
        direction = None
        count = 0
        # print(route)
        new_route = []
        for x in route:
            if x == 'N':
                count += 1
            else:
                if count:
                    new_route.append(count)
                count = 1
                new_route.append(x)
        new_route.append(count)
        self.route = split_route(new_route)
        return self.route

    def get_intersections(self):
        intersections = []
        for y in range(1, len(self.scaffolding)-1):
            line = self.scaffolding[y]
            for x in range(1, len(line)-1):
                if self.is_scaffolding(x+1, y) \
                    and self.is_scaffolding(x,y-1) \
                    and self.is_scaffolding(x,y+1) \
                    and self.is_scaffolding(x,y) \
                    and self.is_scaffolding(x-1,y):
                    intersections.append(x*y)
        return intersections

vacuum = Vacuum(program, video=False)
vacuum.get_scaffolding()
# vacuum.print_scaffolding()
intersections = vacuum.get_intersections()
print("1. {}".format(sum(intersections)))
vacuum.get_route()
vacuum.find_robots()
print("2. {}".format(vacuum.dust))

