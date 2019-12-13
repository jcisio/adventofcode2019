import sys, time

sys.path.append('../common')
import intcode

# Delay time in ms.
ANIMATION_SPEED = 1

TILE_EMPTY = 0
TILE_WALL = 1
TILE_BLOCK = 2
TILE_PADDLE = 3
TILE_BALL = 4

W = 40
H = 20

ball = 0
paddle = 0

def save_tile(x,y,tile):
  screen[(x,y)] = tile

def print_tile(x,y):
  global screen, ball, paddle
  if (x,y)==(-1,0):
    score = screen[(-1, 0)] if (-1,0) in screen else 0
    c = f'Score: {score:05}  Blocks left: {count_blocks():03}'
  elif screen[(x,y)] == TILE_EMPTY:
    c = '  '
  elif screen[(x,y)] == TILE_WALL:
    c = '⬛️'
  elif screen[(x,y)] == TILE_BLOCK:
    c = '⬜️'
  elif screen[(x,y)] == TILE_PADDLE:
    c = '=='
    paddle = x
  elif screen[(x,y)] == TILE_BALL:
    c = '⚫'
    ball = x
  if x==-1:
    pos = '\33[25;0H'
  else:
    pos = '\33[' + str(y+4) + ';' + str(x*2+1) + 'H'
  sys.stdout.write(pos + c + '\33[25;0H')
  sys.stdout.flush()

def print_screen():
  print_tile(-1,0)
  for y in range(H):
    for x in range(W):
      print_tile(x,y)

def print_more(input):
  output = intcode.runIntCode(input)
  for i in range(len(output)//3):
    save_tile(*output[i*3:i*3+3])
    print_tile(*output[i*3:i*3+2])
    if output[i*3+2]:
      # No sleep if it is an erase instruction
      time.sleep(ANIMATION_SPEED/1000)

def count_blocks():
  return sum([tile==TILE_BLOCK for tile in screen.values()])

values = list(map(int, open('d13.in').read().strip().split(',')))
intcode.init(values)
output = intcode.runIntCode([])
screen = {}
for i in range(len(output)//3):
  save_tile(*output[i*3:i*3+3])

sys.stdout.write('\33[2J')
print('\33[0;0HPart 1:', count_blocks())
print_screen()


values[0] = 2
intcode.init(values)
intcode.runIntCode([])
while True:
  input = 1 if ball > paddle else -1 if ball < paddle else 0
  print_more([input])
  if count_blocks()== 0:
    break

print('\33[26;0HPart 2:', screen[(-1, 0)])