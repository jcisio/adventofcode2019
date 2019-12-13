import sys

sys.path.append('../common')
import intcode

TILE_EMPTY = 0
TILE_WALL = 1
TILE_BLOCK = 2
TILE_PADDLE = 3
TILE_BALL = 4

values = list(map(int, open('d13.in').read().strip().split(',')))
intcode.init(values)
output = intcode.runIntCode([])
screen = {}
for i in range(len(output)//3):
  x,y, tile = output[i*3:i*3+3]
  screen[(x,y)] = tile

def print_screen():
  for y in range(20):
    for x in range(40):
      if screen[(x,y)] == TILE_EMPTY:
        c = '  '
      elif screen[(x,y)] == TILE_WALL:
        c = '⬛️'
      elif screen[(x,y)] == TILE_BLOCK:
        c = '⬜️'
      elif screen[(x,y)] == TILE_PADDLE:
        c = '=='
      elif screen[(x,y)] == TILE_BALL:
        c = '⚫'
      print(c, end='')
    print()

print_screen()
print('Part 1:', sum([tile==TILE_BLOCK for tile in screen.values()]))