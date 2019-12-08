def runIntCode(values, input):
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

  values = list(map(int, values))
  input = list(map(int, input))
  numInputs = len(input)
  while True:
    instruction = values[i] % 100
    mode = values[i] // 100
    modes = (mode % 10, (mode // 10) % 10, mode // 100)
    if instruction == 99:
      break
    elif instruction == 1 or instruction == 2:
      a = values[values[i+1]] if modes[0] == 0 else values[i+1]
      b = values[values[i+2]] if modes[1] == 0 else values[i+2]
      values[values[i+3]] = a+b if instruction == 1 else a*b
      i += 4
    elif instruction == 3:
      if not input:
        break
      values[values[i+1]] = input.pop()
      i += 2
    elif instruction == 4:
      a = values[values[i+1]] if modes[0] == 0 else values[i+1]
      output.append(a)
      i += 2
    elif instruction == 5 or instruction == 6:
      a = values[values[i+1]] if modes[0] == 0 else values[i+1]
      b = values[values[i+2]] if modes[1] == 0 else values[i+2]
      if (a == 0) == (instruction == 6):
        i = b
      else:
        i += 3
    elif instruction == 7 or instruction == 8:
      a = values[values[i+1]] if modes[0] == 0 else values[i+1]
      b = values[values[i+2]] if modes[1] == 0 else values[i+2]
      values[values[i+3]] = 1 if (instruction == 7 and a < b) or (instruction == 8 and a == b) else 0
      i += 4

  if  HaltOnFirstOutput:
    output = output[numInputs-2:]

  return ' '.join(map(str, output))

import fileinput
data = [line.strip().split(',') for line in fileinput.input()]
print(runIntCode(data[0], data[1]))
