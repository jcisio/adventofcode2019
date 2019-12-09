values = []
relative_base = 0


# Param position with mode 0, 1, 2
def getParam(mode, position):
  global relative_base
  if (mode == 0):
    target_position = values[position]
  elif (mode == 1):
    target_position = position
  else:
    target_position = values[position] + relative_base
  if target_position not in values:
    values[target_position] = 0
  return values[target_position]


# Write instructions do not allow direct value
def writeToPosition(mode, position, value):
  if mode == 0 or mode == 1:
    target_position = values[position]
  else:
    target_position = values[position] + relative_base
  values[target_position] = value


def runIntCode(input):
  global values, relative_base
  output = []
  i = 0

  # Whether this program halts on the first output.
  # By default, it only halts on instruction 99 and it could produce
  # multiple output. However, to solve day 7 part 2, it requires that
  # the intCode could be pause and resume after each output. To do so,
  # as an external program, a special input is used. If the last input
  # is HaltOnFirstOutput, then it will start at position N and
  # halt at the first output, and it also print the current position so
  # that it could be resumed.
  HaltOnFirstOutput = False
  if input[-1] == 'HaltOnFirstOutput':
    input.pop()
    HaltOnFirstOutput = True

  # Use dict to cope with arbitrarily large memory position.
  values = {i : int(values[i]) for i in range(len(values))}

  input = list(map(int, input))
  numInputs = len(input)
  while True:
    instruction = values[i] % 100
    mode = values[i] // 100
    modes = (mode % 10, (mode // 10) % 10, mode // 100)
    if instruction == 99:
      break
    elif instruction == 1 or instruction == 2:
      a = getParam(modes[0], i+1)
      b = getParam(modes[1], i+2)
      writeToPosition(modes[2], i+3, a+b if instruction == 1 else a*b)
      i += 4
    elif instruction == 3:
      if not input:
        break
      writeToPosition(modes[0], i+1, input.pop())
      i += 2
    elif instruction == 4:
      a = getParam(modes[0], i+1)
      output.append(a)
      i += 2
    elif instruction == 5 or instruction == 6:
      a = getParam(modes[0], i+1)
      b = getParam(modes[1], i+2)
      if (a == 0) == (instruction == 6):
        i = b
      else:
        i += 3
    elif instruction == 7 or instruction == 8:
      a = getParam(modes[0], i+1)
      b = getParam(modes[1], i+2)
      writeToPosition(modes[2], i+3, 1 if (instruction == 7 and a < b) or (instruction == 8 and a == b) else 0)
      i += 4
    elif instruction == 9:
      a = getParam(modes[0], i+1)
      relative_base += a
      i += 2

  if  HaltOnFirstOutput:
    output = output[numInputs-2:]

  return ' '.join(map(str, output))


import fileinput
values, input = [line.strip().split(',') for line in fileinput.input()]
print(runIntCode(input))
