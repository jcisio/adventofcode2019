import sys

sys.path.append('../common')
import intcode

def get_scaffolds(values):
    intcode.init(values)
    output = intcode.runIntCode([])
    output = list(map(chr, output))
    scaffolds = ''.join(output).strip().split('\n')
    return scaffolds

def part1(scaffolds):
    x,y = len(scaffolds[0]), len(scaffolds)

    scaffold = '#<^>v'
    intersections = []
    for j in range(1, y-1):
        for i in range(1, x-1):
            around = scaffolds[j][i] + scaffolds[j-1][i] + scaffolds[j+1][i] + scaffolds[j][i-1] + scaffolds[j][i+1]
            if all([c in scaffold for c in around]):
                intersections.append(i*j)
    return sum(intersections)

with open('d17.in') as f:
    input = f.read().strip()

values = input.split(',')
scaffolds = get_scaffolds(values)
print('\n'.join(scaffolds))

print('Part 1:', part1(scaffolds))
