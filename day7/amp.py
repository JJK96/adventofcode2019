from intcode import *
import threading

def output_callback(output, amplifier):
    amplifier.inputs.put(output)

def amp(program, phases, inputs):
    amps = []
    for name, phase in enumerate(phases):
        amps.append(Computer(program, [phase], name=name))
    for i in range(len(amps)-1):
        amps[i].output_callback = lambda output, amplifier=amps[i+1]: output_callback(output, amplifier)
        amps[i].start()
    amps[-1].output_callback = lambda output, amplifier=amps[0]: output_callback(output, amplifier)
    amps[-1].start()
    for i in inputs:
        amps[0].inputs.put(i)
    for a in amps:
        a.thread.join()
    
    return list(amps[0].inputs.queue)

def unique(x):
    return len(set(x)) == len(x)

def phases_generator(num_phases, ranges):
    low, high = ranges
    if num_phases > 0:
        for x in range(low, high):
            for y in phases_generator(num_phases -1, ranges):
                y = list(y)
                y.append(x)
                yield y
    else:
        yield []


def get_max_output(program, ranges, num_phases=5):
    max = 0
    max_phases = []
    for phases in phases_generator(num_phases, ranges):
        if unique(phases):
            outputs = amp(program, phases, [0])
            if outputs[0] > max:
                max = outputs[0]
                max_phases = phases
    return (max, max_phases)

with open('input', 'r') as f:
    input_string = f.read()
program = convert(input_string)
print("1: " + str(get_max_output(program, (0,5))[0]))
print("2: " + str(get_max_output(program, (5,10))[0]))
