import intcode
import os
import time
import numpy as np

class Arcade:
    def __init__(self, input, screen_size, add_quarters=True, human_input=False, do_print=True):
        self.human_input = human_input
        self.do_print = do_print
        self.outputs = []
        x, y = screen_size
        self.screen = [[' ' for _ in range(x)] for _ in range(y)]
        if add_quarters:
            input[0] = 2
        output_callback=lambda output, self=self: self.handle_output(output)
        input_callback=self.get_input
        self.computer = intcode.Computer(input, input_callback, output_callback=output_callback)
        self.score = 0

    def get_input(self):
        if self.human_input:
            line = input()
            if len(line) == 0:
                return 0
            char = line[0]
            if char == 'a':
                return -1
            elif char == 'r':
                return 1
        else:
            if self.do_print:
                time.sleep(0.05)
            x, y = self.ball
            xp, yp = self.paddle
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
        if self.do_print:
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

size = (43,22)
program = intcode.convert(input_string)
arcade = Arcade(program, size, add_quarters=False, do_print=False)
arcade.start()
arcade.computer.thread.join()
block_tiles = len([x for x in np.array(arcade.screen).flatten() if x == '#'])
print(f"1. {block_tiles}")
arcade = Arcade(program, size, do_print=False)
arcade.start()
arcade.computer.thread.join()
print(f"2. {arcade.score}")
