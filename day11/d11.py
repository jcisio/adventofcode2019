import sys

sys.path.append('../common')
import intcode

values = list(map(int, open('d11.in', 'r').read().strip().split(',')))
values = {i: int(values[i]) for i in range(len(values))}


def paint_panels(input):
  intcode.init(values)
  points = {}
  x, y, direction = 0, 0, 0
  while True:
    output = intcode.runIntCode(input)
    if not output:
      break
    points[(x, y)] = output[0]
    direction = (direction + (-1 if output[1] == 0 else 1)) % 4
    if direction == 0:
      y += 1
    elif direction == 1:
      x += 1
    elif direction == 2:
      y -= 1
    elif direction == 3:
      x -= 1
    input = [0 if (x, y) not in points else points[(x, y)]]
  return points


print('Part 1:', len(paint_panels([0])))

print('Part 2:')
points = paint_panels([1])
x1 = min([p[0] for p in points])
y1 = min([p[1] for p in points])
x2 = max([p[0] for p in points])
y2 = max([p[1] for p in points])
for y in range(y2, y1-1, -1):
  line = []
  for x in range(x1, x2+1):
    color = points[(x,y)] if (x,y) in points else 0
    line.append('⬛️' if color else '⬜️')
  print(''.join(line))

