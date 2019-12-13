import intcode
import os
import time

HUMAN_INPUT = False

class Arcade:
    def __init__(self, input, screen_size):
        self.outputs = []
        x, y = screen_size
        self.screen = [[' ' for _ in range(x)] for _ in range(y)]
        input[0] = 2
        output_callback=lambda output, self=self: self.handle_output(output)
        input_callback=self.get_input
        self.computer = intcode.Computer(input, input_callback, output_callback=output_callback)
        self.score = 0

    def get_input(self):
        if HUMAN_INPUT:
            line = input()
            if len(line) == 0:
                return 0
            char = line[0]
            if char == 'a':
                return -1
            elif char == 'r':
                return 1
        else:
            x, y = self.ball
            xp, yp = self.paddle
            time.sleep(0.005)
            if x > xp:
                return 1
            elif x == xp:
                return 0
            else:
                return -1

    def start(self):
        self.computer.start()

    def handle_output(self, output):
        self.outputs.append(output)
        if len(self.outputs) == 3:
            x = self.outputs[0]
            y = self.outputs[1]
            pos = (x,y)
            if pos == (-1, 0):
                self.score = self.outputs[2]
            else:
                id = self.outputs[2]
                if id == 4:
                    self.ball = pos
                if id == 3:
                    self.paddle = pos
                self.screen[y][x] = self.id_to_char(id)
            self.outputs = []
            self.draw()

    def id_to_char(self, id):
        if id == 0:
            return ' '
        elif id == 1:
            return '█'
        elif id == 2:
            return '#'
        elif id == 3:
            return '='
        elif id == 4:
            return 'o'
        else:
            print(id)

    def draw(self):
        os.system('clear')
        print(self.score)
        string = ""
        for line in self.screen:
            for char in line:
                string += char
            string += "\n"
        print(string)

with open('input','r') as f:
    input_string = f.read()

program = intcode.convert(input_string)
arcade = Arcade(program, (43,22))
arcade.start()
