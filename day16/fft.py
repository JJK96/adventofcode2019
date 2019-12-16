from math import log, ceil, floor

def fft(input, phases, offset):
    if phases == 0:
        return input
    pattern = [0, 1, 0, -1]
    prev_phase = fft(input, phases -1, offset)
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

with open('input') as f:
    input = f.read()[:-1]

to_skip = int(input[:7])
input = [int(x) for x in input]
res = fft(input, 100, 0)
print("1. " + ''.join([str(x) for x in res[:8]]))
input *= 10000
res = fft(input[to_skip:], 100, to_skip)
print("2. " + ''.join([str(x) for x in res[:8]]))
