from intcode import *

class Location:
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.faces = ["up", "left", "down", "right"]
        self.facing = self.faces.index(facing)

    def turn(self, direction):
        if direction == 0:
            # left
            self.facing = (self.facing + 1) % len(self.faces)
        else:
            self.facing = (self.facing - 1) % len(self.faces)

    def move(self):
        direction = self.faces[self.facing]
        if direction == "up":
            self.y -= 1
        elif direction == "left":
            self.x -= 1
        elif direction == "down":
            self.y += 1
        elif direction == "right":
            self.x += 1

    @property
    def location(self):
        return (self.x,self.y)

def get_current_color(location):
    return panels.get(location.location, 0)

def handle_output(self, output):
    self.outputs.append(output)
    if len(self.outputs) == 2:
        new_color = self.outputs[0]
        panels[self.location.location] = new_color
        self.location.turn(self.outputs[1])
        self.location.move()
        current_color = get_current_color(self.location)
        self.outputs = []
        self.inputs.put(current_color)

def draw_registration_identifier(panels):
    x_range = [0,0]
    y_range = [0,0]
    for k in panels.keys():
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
    for k, v in panels.items():
        x, y = k
        x -= x_range[0]
        y -= y_range[0]
        if v == 1:
            map[y][x] = "█"
    string = ""
    for line in map:
        for char in line:
            string += char
        string += "\n"
    return string

with open('input', 'r') as f:
    input_string = f.read()
input = convert(input_string)

panels = {}

robot = Computer(input)
robot.location = Location(0,0,"up")
current_color = get_current_color(robot.location)
robot.inputs.put(current_color)
robot.outputs = []
robot.handle_output = handle_output
robot.output_callback = lambda output, robot=robot: handle_output(robot, output)
robot.start()
robot.thread.join()
print("1. " + str(len(panels.keys())))

panels = {}
panels[(0,0)] = 1
robot = Computer(input)
robot.location = Location(0,0,"up")
current_color = get_current_color(robot.location)
robot.inputs.put(current_color)
robot.outputs = []
robot.handle_output = handle_output
robot.output_callback = lambda output, robot=robot: handle_output(robot, output)
robot.start()
robot.thread.join()

print("2.")
print(draw_registration_identifier(panels))
