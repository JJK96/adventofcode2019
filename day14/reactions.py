import math

def parse_chemical(chemical):
    amount, chemical = chemical.split()
    return (int(amount), chemical)

def parse_input(input):
    reactions = {}
    for line in input.split('\n'):
        ins, out = line.split('=>')
        amount, out = parse_chemical(out.strip())
        ins = [parse_chemical(x.strip()) for x in ins.split(', ')]
        assert reactions.get(out) is None, "not unique"
        reactions[out] = (amount, ins)
    return reactions

def multiply_recipe(recipe, factor):
    for i in range(len(recipe)):
        a, b = recipe[i]
        recipe[i] = (a*factor, b)
    return recipe

surplus = {}
def required_ore(reactions, chemical, needed):
    if chemical == 'ORE':
        return needed
    current_surplus = surplus.get(chemical, 0)
    if current_surplus >= needed:
        current_surplus -= needed
        needed = 0
    else:
        needed -= current_surplus
        current_surplus = 0
    amount, recipe = reactions[chemical]
    times = math.ceil(needed/amount)
    mysurplus = times*amount - needed
    surplus[chemical] = current_surplus + mysurplus
    total = 0
    for amount, chem in recipe:
        total += required_ore(reactions, chem, amount*times)
    return total

def max_fuel(ore):
    amount = ore//required
    step = amount
    while step != 0:
        ore_required = required_ore(reactions, 'FUEL', amount+step)
        if ore_required > ore:
            step //= 2
        else:
            amount += step
    return amount

with open('input') as f:
    input=f.read()[:-1]

reactions = parse_input(input)
required = required_ore(reactions, 'FUEL', 1)
print("1. " + str(required))
ore = 10**12
print("2. " + str(max_fuel(ore)))
