width, height = 25, 6
with open('input', 'r') as f:
    input_string = f.read()[:-1]
layer_size = width*height
num_layers = len(input_string)/layer_size

def one(input_string):
    counts = []
    for i in range(0, len(input_string), layer_size):
        layer = input_string[i:i+layer_size]
        count = [0,0,0]
        for num in layer:
            count[int(num)] += 1
        counts.append(count)

    least_zero = min(counts, key=lambda x: x[0])
    return least_zero[1]*least_zero[2]

print(one(input_string))

def print_image(image, width, height):
    string = ""
    for i in range(0, len(image), width):
        line = image[i:i+width]
        for c in line:
            string += "██" if c == 1 else "  "
        string += "\n"
    print(string)

def render_image(input_string, width, height):
    layer_size = width*height
    image = [2 for _ in range(layer_size)]
    for i in range(0, len(input_string), layer_size):
        layer = input_string[i:i+layer_size]
        for j in range(len(layer)):
            if image[j] == 2:
                image[j] = int(layer[j])
    print_image(image, width, height)

render_image(input_string, width, height)
