import sys

sys.path.append('../common')
import intcode

values = list(map(int, open('d13.in').read().strip().split(',')))
intcode.init(values)
output = intcode.runIntCode([])
screen = {}
for i in range(len(output)//3):
  x,y, tile = output[i*3:i*3+3]
  screen[(x,y)] = tile
print('Part 1:', sum([tile==2 for tile in screen.values()]))