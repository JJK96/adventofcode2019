from math import log, ceil, floor

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

patterns = {}
def recursive_fft(input, phases, indexes):
    if phases == 0:
        output = {}
        for i in indexes:
            output[i] = int(input[i])
        return output
    pattern = [0, 1, 0, -1]
    new_indexes = set()
    for i in indexes:
        pattern_row = patterns.get(i, {})
        if len(pattern_row) == 0:
            for j in range(i, len(input)):
                pattern_index = ((j+1)//(i+1)) % len(pattern)
                pattern_row[j] = pattern[pattern_index]
            patterns[i] = pattern_row
        for k in pattern_row.keys():
            new_indexes.add(k)
    prev_phase = recursive_fft(input, phases - 1, new_indexes)
    output = {}
    for i in indexes:
        pattern = patterns[i]
        val = 0
        for index, factor in pattern.items():
            val += prev_phase[index] * factor
        output[i] = int(str(val)[-1])
    return output

def rec1(input, phases, offset):
    if phases == 0:
        return input
    pattern = [0, 1, 0, -1]
    prev_phase = rec1(input, phases -1, offset)
    length = len(prev_phase)+offset
    output = []
    for i in range(offset, length//2):
        val = 0
        for j in range(i, len(prev_phase)):
            pattern_index = ((j+1)//(i+1)) % len(pattern)
            val += pattern[pattern_index] * prev_phase[j-offset]
        val = str(val)
        val = val[-1]
        output.append(int(val))
    output1 = []
    val = 0
    end = max(length//2, offset)
    for i in range(length-1, end-1, -1):
        val += prev_phase[i-offset]
        output1.append(int(str(val)[-1]))
    return output + output1[::-1]

def lars(input, phases):
    a = input
    n = len(input)
    for phase in range(phases):
        b = []
        for t in range(1, n+1):
            C = floor((n-4*t+1)/(4*t))
            val = 0
            if t <= ceil((n-1)/4):
                part1 = sum([a[t+m-1] - a[3*t+m-1] for m in range(t)])
                part2 = sum([a[4*t*i+m+t-1] - a[4*t*i+m+3*t-1] for m in range(t) for i in range(1, C+1)])
                val = part1 + part2
            elif ceil((n-1)/4) < t <= ceil((n-1)/2):
                part1 = sum([a[t+m-1] for m in range(t)])
                part2 = sum([a[m-1] for m in range(3*t, n+1)])
                val = part1 - part2
            else:
                val = sum([a[m-1] for m in range(t, n+1)])
            b.append(int(str(val)[-1]))
        a = b
    return a

with open('input') as f:
    input = f.read()[:-1]

to_skip = int(input[:7])
input = [int(x) for x in input]
res = rec1(input, 100, 0)
print("1. " + ''.join([str(x) for x in res[:8]]))
input *= 10000
res = rec1(input[to_skip:], 100, to_skip)
print("2. " + ''.join([str(x) for x in res[:8]]))
