from intcode import *
import threading

def output_callback(output, amplifier):
    # print(f"thread {threading.get_ident()}")
    # print(f"handing {output} to {amplifier.name}")
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

def get_max_output(program):
    max = 0
    max_phases = []
    for phase0 in range(5,10):
        for phase1 in range(5,10):
            for phase2 in range(5,10):
                for phase3 in range(5,10):
                    for phase4 in range(5,10):
                        phases = [phase0, phase1, phase2, phase3, phase4]
                        if unique(phases):
                            outputs = amp(program, phases, [0])
                            if outputs[0] > max:
                                max = outputs[0]
                                max_phases = phases
    return (max, max_phases)

with open('input', 'r') as f:
    input_string = f.read()
program = convert(input_string)
print(get_max_output(program))
