f = open('d02.in', 'r')
values = list(map(int, f.read().strip().split(',')))

def runIntCode(values, a, b):
  i = 0
  values[1] = a
  values[2] = b
  while True:
    if values[i] == 99:
      break
    if values[i] == 1:
      values[values[i+3]] = values[values[i+1]] + values[values[i+2]]
    else:
      values[values[i+3]] = values[values[i+1]] * values[values[i+2]]
    i += 4
  return values[0]

print('Part 1: ', runIntCode(values.copy(), 12, 2))

for i in range(100):
  for j in range(100):
    if runIntCode(values.copy(), i, j) == 19690720:
      print('Part 2: ', i*100+j)
      break
