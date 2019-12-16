from math import log, ceil

def fft(input, phases):
    input = str(input)
    pattern = [0, 1, 0, -1]
    for phase in range(phases):
        new_input = ""
        for i in range(1, len(input)+1):
            val = 0
            counter = 0
            pattern_index = 0
            for j in range(len(input)):
                counter += 1
                if counter == i:
                    pattern_index += 1
                    counter = 0
                pattern_index %=  len(pattern)
                res = pattern[pattern_index] * int(input[j])
                val += res
            new_input += str(val)[-1]
        input = new_input
    return input

with open('input') as f:
    input = f.read()[:-1]

# input *= 10000
res = fft(input, 100)
print(res[:8])
# to_skip = int(input[:7])
# print(res[to_skip:to_skip+8])
