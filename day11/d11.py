import sys
sys.path.append('../common')
import intcode

values = list(map(int, open('d11.in', 'r').read().strip().split(',')))
intcode.values = {i : int(values[i]) for i in range(len(values))}

points = {}
x, y, direction = 0, 0, 0
output_length = 0
input = [0]
while True:
    output = intcode.runIntCode(input)
    if not output:
        break
    points[(x,y)] = output[0]
    direction = (direction + (-1 if output[1] == 0 else 1)) % 4
    if direction == 0:
        y += 1
    elif direction == 1:
        x += 1
    elif direction == 2:
        y -= 1
    elif direction == 3:
        x -= 1
    input = [0 if (x,y) not in points else points[(x,y)]]

print('Part 1:', len(points))
