orbit_map = {}
space_objects = {}

class SpaceObject:
    def __init__(self, name):
        self.name = name
        orbiting_objects = orbit_map.get(name, [])
        self.orbiting_objects = {}
        self.orbit_num = 0
        for orbiting_object in orbiting_objects:
            space_object = SpaceObject(orbiting_object)
            space_object.orbits = self
            self.orbiting_objects[space_object.name] = space_object
            self.orbit_num += space_object.orbit_num + 1
        space_objects[self.name] = self

    def get_path(self):
        if self.name == "COM":
            return ["COM"]
        else:
            path = self.orbits.get_path()
            path.insert(0, self.name)
            return path

    def __getitem__(self, index):
        return self.orbiting_objects[index]

    def __repr__(self):
        return self.name + ": " + str([name for name in self.orbiting_objects.keys()])

    def __str__(self):
        string = f"{str(self.name)}\n"
        for orbiting_object in self.orbiting_objects.values():
            string += "\n".join([f" {object}" for object in str(orbiting_object).split("\n")])
        return string

def insert_orbit(orbit):
    orbiting, space_object = orbit.split(")")
    orbiting_objects = orbit_map.get(orbiting, [])
    orbiting_objects.append(space_object)
    orbit_map[orbiting] = orbiting_objects


def get_num_transfers(mypath, sanpath):
    for i, so in enumerate(mypath[1:]):
        for j, so1 in enumerate(sanpath[1:]):
            if so == so1:
                return i+j


input = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""

with open('input', 'r') as f:
    input = f.read()

for line in input.split():
    insert_orbit(line)

com = SpaceObject("COM")
orbit_num = 0
for space_object in space_objects.values():
    orbit_num += space_object.orbit_num
print("1: " + str(orbit_num))

mypath = space_objects["YOU"].get_path()
sanpath = space_objects["SAN"].get_path()

print("2: " + str(get_num_transfers(mypath, sanpath)))
