from intcode import *

outputs = []
def handle_output(output):
    outputs.append(output)

def draw_tiles(outputs):
    screen = {}
    for i in range(0, len(outputs), 3):
        x = outputs[i]
        y = outputs[i+1]
        pos = (x,y)
        id = outputs[i+2]
        screen[pos] = id
    return screen

with open('input','r') as f:
    input = f.read()

input = convert(input)
arcade = Computer(input, output_callback=handle_output)
arcade.run()
screen = draw_tiles(outputs)
block_tiles = len([x for x in screen.values() if x == 2])
