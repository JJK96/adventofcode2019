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

with open('input') as f:
    input = f.read()[:-1]

# input = "19617804207202209144916044189917"
# to_skip = int(input[:7])
# input *= 10000
# print(res[to_skip:to_skip+8])
# myrange = range(to_skip, to_skip+8)
myrange = range(8)
res = recursive_fft(input, 100, set(myrange))
output = ""
for i in myrange:
    output += str(res[i])
print(output)
