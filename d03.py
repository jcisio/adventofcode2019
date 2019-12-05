f = open('d03.in', 'r')
wire1 = f.readline().strip().split(',')
wire2 = f.readline().strip().split(',')

directions = {
  'R': (1, 0),
  'L': (-1, 0),
  'U': (0, 1),
  'D': (0, -1),
}
plan = {}

def trace(wire, value):
  global distance, plan, directions
  x, y = 0, 0
  for move in wire:
    direction = directions[move[0]]
    steps = int(move[1:])
    for i in range(steps):
      x += direction[0]
      y += direction[1]
      if (y,x) in plan:
        if plan[(y,x)] != value:
          plan[(y,x)] = 'x'
          distance = abs(x)+abs(y) if distance is None else min(distance, abs(x)+abs(y))
      else:
        plan[(y,x)] = value


def trace2(wire):
  global distance_set, plan, directions
  x, y = 0, 0
  wire_distance = 0
  for move in wire:
    direction = directions[move[0]]
    steps = int(move[1:])
    for i in range(steps):
      x += direction[0]
      y += direction[1]
      wire_distance += 1
      if plan[(y,x)] == 'x':
        if (y,x) not in distance_set:
          distance_set[(y,x)] = 0
        distance_set[(y, x)] += wire_distance

distance = None
trace(wire1, '-')
trace(wire2, '+')
print('Part 1: ', distance)

distance_set = {}
trace2(wire1)
trace2(wire2)
print('Part 2: ', min(distance_set.values()))
