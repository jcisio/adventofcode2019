import math

recipes = {}
materials = {'ORE'}
for line in open('d14.in').readlines():
    left, right = line.strip().split(' => ')
    output = right.split()
    recipes[output[1]] = {
        'quantity': int(output[0]),
        'ingredients': {item[1]: int(item[0]) for item in [item.split() for item in left.split(', ')]}
    }
    materials.add(output[1])

distance = {'ORE': 0}
while len(distance) < len(materials):
    for material in materials:
        if material in distance:
            continue
        if not all([i in distance for i in recipes[material]['ingredients'].keys()]):
            continue
        distance[material] = max([distance[i] for i in recipes[material]['ingredients'].keys()]) + 1


def required_ore(fuel):
    global materials, recipes, distance
    needed = {'FUEL': fuel}
    while len(needed) > 1 or 'ORE' not in needed:
        material = max(needed, key=lambda x: distance[x])
        quantity = needed[material]
        del needed[material]
        base_quantity, ingredients = recipes[material].values()
        for a, b in ingredients.items():
            if a not in needed:
                needed[a] = 0
            needed[a] += math.ceil(quantity/base_quantity)*b
    return needed['ORE']

def search_fuel_target(ore):
    one_unit = required_ore(1)
    target = ore//one_unit
    used_ore = required_ore(target)
    while True:
        target += (ore-used_ore)//one_unit + 1
        used_ore = required_ore(target)
        if used_ore > ore:
            break
    return target - 1


print('Part 1:', required_ore(1))
print('Part 2:', search_fuel_target(1000000000000))
