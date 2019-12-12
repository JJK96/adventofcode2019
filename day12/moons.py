import re
import numpy as np

AXIS_NUM = 3

class Moon:
    def __init__(self, pos):
        self.pos = np.array(pos)
        self.vel = np.array([0 for _ in range(AXIS_NUM)])

    def apply_vel(self):
        self.pos += self.vel

    @property 
    def pot(self):
        return sum(abs(self.pos))

    @property 
    def kin(self):
        return sum(abs(self.vel))

    def __repr__(self):
        string = "(pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>)".format(self.pos[0], self.pos[1], self.pos[2],
            self.vel[0], self.vel[1], self.vel[2])
        return string

def update(moons):
    for i in range(len(moons)):
        a = moons[i]
        for j in range(i+1, len(moons)):
            b = moons[j]
            vel_update = []
            for axis in range(AXIS_NUM):
                if a.pos[axis] < b.pos[axis]:
                    vel_update.append(1)
                elif a.pos[axis] > b.pos[axis]:
                    vel_update.append(-1)
                else:
                    vel_update.append(0)
            vel_update = np.array(vel_update)
            a.vel += vel_update
            b.vel -= vel_update
        a.apply_vel()

def print_moons(moons):
    for moon in moons:
        print(moon)

def update_multiple(moons, steps, do_print=False):
    if do_print:
        print("After 0 steps:")
        print_moons(moons)
    for i in range(1, steps+1):
        update(moons)
        if do_print:
            print(f"After {i} steps:")
            print_moons(moons)

def get_state(moons):
    xs = []
    ys = []
    zs = []
    for moon in moons:
        x, y, z = moon.pos
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return xs, ys, zs

def equal(state1, state2):
    xs = state1[0] == state2[0]
    ys = state1[1] == state2[1]
    zs = state1[2] == state2[2]
    return xs, ys, zs

def total_energy(moons):
    total = 0
    for moon in moons:
        energy = moon.pot * moon.kin
        total += energy
    return total

def find_length(moons):
    initial = get_state(moons)
    i = 0
    lengths = [0 for _ in range(AXIS_NUM)]
    while any([x == 0 for x in lengths]):
        update(moons)
        i += 1
        state = get_state(moons)
        comparison = equal(state,initial)
        for j in range(len(comparison)):
            if comparison[j] and lengths[j] == 0:
                lengths[j] = i+1
    return np.lcm.reduce(lengths)

def convert(input):
    moons = []
    for line in input.split('\n'):
        search = re.search(moon_regex, line)
        if search is not None:
            pos = [int(x) for x in search.groups()]
            moons.append(Moon(pos))
    return moons

with open('input','r') as f:
    input = f.read()

moon_regex = r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>'

moons = convert(input)
update_multiple(moons, 1000, False)
print("1. " + str(total_energy(moons)))
moons = convert(input)
print("2. " + str(find_length(moons)))
