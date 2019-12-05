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


def computer(memory):
    ip = 0
    while True:
        opcode, modes = decode_opcode(memory[ip])
        # print(f"{opcode=}")
        # print(f"{memory[ip:ip+5]=}")
        if opcode == 99:
            return memory
        elif opcode == 3 or opcode == 4:
            par1 = memory[ip + 1]
            if opcode == 3:
                memory[par1] = get_input()
            else:
                print(memory[par1])
            ip += 2
            continue
        par1, par2 = get_values(memory[ip + 1:ip + 3], modes, memory)
        if opcode == 1 or opcode == 2:
            dest = memory[ip + 3]
            memory[dest] = par1 + par2 if opcode == 1 else par1 * par2
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
            memory[memory[ip + 3]] = res
            ip += 4


def compute(noun, verb, memory):
    memory[1] = noun
    memory[2] = verb
    return computer(memory)


def convert(string):
    return [int(x) for x in string.split(',')]


with open('input', 'r') as f:
    input_string = f.read()

for id in [1, 5]:
    input = convert(input_string)
    print(f"{id=}")

    def get_input():
        return id

    computer(input)
