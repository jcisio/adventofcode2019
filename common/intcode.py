def init(new_values):
  global values, output, relative_base, i

  # Convert list to dict if necessary. We use dict for space efficiency.
  if type(new_values) is list:
    new_values = {i: int(new_values[i]) for i in range(len(new_values))}
  values = new_values
  output = []
  relative_base = 0
  i = 0

# Param position with mode 0, 1, 2
def getParam(mode, position):
  global relative_base, values
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
  global values, output, relative_base, i
  new_output = []
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
      writeToPosition(modes[0], i+1, int(input.pop(0)))
      i += 2
    elif instruction == 4:
      a = getParam(modes[0], i+1)
      output.append(a)
      new_output.append(a)
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
      relative_base = relative_base + a
      i += 2

  return new_output
