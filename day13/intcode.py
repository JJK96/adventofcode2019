import copy
import queue
import threading

def decode_opcode(opcode):
    return (opcode % 100, opcode // 100)


class Computer:
    def __init__(self, program, inputs=[], output_callback=(lambda x: print(x)), name=None):
        self.inputs = queue.Queue()
        for i in inputs:
            self.inputs.put(i)
        self.outputs = []
        self.memory = copy.copy(program)
        self.memory += [0]*2**20
        self.output_callback = output_callback
        self.name = name
        self.relative_base = 0

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        ip = 0
        while True:
            opcode, modes = decode_opcode(self.memory[ip])
            if opcode == 99:
                return self.memory
            if opcode == 3:
                par1 = self.get_values(self.memory[ip + 1:ip + 2], modes)[1][0]
                self.memory[par1] = self.inputs.get()
                ip += 2
                continue
            par1 = self.get_values(self.memory[ip + 1:ip + 2], modes)[0][0]
            if opcode == 4:
                self.output_callback(par1)
                ip += 2
                continue
            elif opcode == 9:
                self.relative_base += par1
                ip += 2
                continue
            values, addresses = self.get_values(self.memory[ip+1:ip+4], modes)
            par1, par2, _ = values
            dest = addresses[2]
            if opcode == 1 or opcode == 2:
                self.memory[dest] = par1 + par2 if opcode == 1 else par1 * par2
                ip += 4
                continue
            elif opcode == 5 or opcode == 6:
                if par1 != 0 and opcode == 5 or par1 == 0 and opcode == 6:
                    ip = par2
                else:
                    ip += 3
                continue
            elif opcode == 7 or opcode == 8:
                if opcode == 7:
                    check = par1 < par2
                else:
                    check = par1 == par2
                res = 1 if check else 0
                self.memory[dest] = res
                ip += 4

    def get_values(self, params, modes):
        values = []
        addresses = []
        for param in params:
            mode = modes % 10
            modes = modes // 10
            if mode == 0:
                addresses.append(param)
                values.append(self.memory[param])
            elif mode == 1:
                addresses.append(param)
                values.append(param)
            elif mode == 2:
                addresses.append(param+self.relative_base)
                values.append(self.memory[param+self.relative_base])
        return values, addresses



def compute(noun, verb, memory):
    memory[1] = noun
    memory[2] = verb
    computer = Computer(memory)
    return computer.run()


def convert(string):
    return [int(x) for x in string.split(',')]


if __name__ == "__main__":
    with open('input', 'r') as f:
        input_string = f.read()
    input = convert(input_string)

    output = []
    computer = Computer(input, [1], output_callback=lambda x, output=output: output.append(x))
    computer.run()
    print(f"1. {output[0]}")
    output = []
    computer = Computer(input, [2], output_callback=lambda x, output=output: output.append(x))
    computer.run()
    print(f"2. {output[0]}")
