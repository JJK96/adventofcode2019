import copy
import queue
import threading

def decode_opcode(opcode):
    return (opcode % 100, opcode // 100)


def get_values(params, modes, memory):
    values = []
    for param in params:
        mode = modes % 10
        modes = modes // 10
        if mode == 0:
            values.append(memory[param])
        else:
            values.append(param)
    return values


class Computer:
    def __init__(self, program, inputs=[], output_callback=(lambda x: print(x)), name=None):
        self.inputs = queue.Queue()
        for i in inputs:
            self.inputs.put(i)
        self.outputs = []
        self.memory = copy.copy(program)
        self.output_callback = output_callback
        self.name = name

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        ip = 0
        while True:
            opcode, modes = decode_opcode(self.memory[ip])
            # print(f"{opcode=}")
            # print(f"{self.memory[ip:ip+5]=}")
            if opcode == 99:
                return self.memory
            elif opcode == 3 or opcode == 4:
                par1 = self.memory[ip + 1]
                if opcode == 3:
                    # print(f"{self.name} waiting for input")
                    self.memory[par1] = self.inputs.get()
                else:
                    output = self.memory[par1]
                    self.output_callback(output)
                ip += 2
                continue
            par1, par2 = get_values(self.memory[ip + 1:ip + 3], modes, self.memory)
            if opcode == 1 or opcode == 2:
                dest = self.memory[ip + 3]
                self.memory[dest] = par1 + par2 if opcode == 1 else par1 * par2
                ip += 4
            elif opcode == 5 or opcode == 6:
                if par1 != 0 and opcode == 5 or par1 == 0 and opcode == 6:
                    ip = par2
                else:
                    ip += 3
            elif opcode == 7 or opcode == 8:
                if opcode == 7:
                    check = par1 < par2
                else:
                    check = par1 == par2
                res = 1 if check else 0
                self.memory[self.memory[ip + 3]] = res
                ip += 4


def compute(noun, verb, memory):
    memory[1] = noun
    memory[2] = verb
    computer = Computer(memory)
    return computer.run()


def convert(string):
    return [int(x) for x in string.split(',')]


if __name__ == "__main__":
    with open('input1', 'r') as f:
        input_string = f.read()
    input = convert(input_string)

    for id in [1, 5]:
        print(f"{id=}")

        computer = Computer(input, [id])
        computer.run()
