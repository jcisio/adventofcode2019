f = open('d04.in', 'r')
(start, end) = map(int, f.read().strip().split('-'))

def isPassword(password):
  if password < 100000 or password > 999999:
    return False
  hasDouble = False
  password = str(password)
  for i in range(5):
    if password[i] > password[i+1]:
      return False
    elif password[i] == password[i+1]:
      hasDouble = True
  return hasDouble


def isPassword2(password):
  if password < 100000 or password > 999999:
    return False
  hasDouble = False
  password = str(password)
  for i in range(5):
    if password[i] > password[i+1]:
      return False
    elif password[i] == password[i+1] and (i == 0 or password[i] != password[i-1]) and (i==4 or password[i] != password[i+2]):
      hasDouble = True
  return hasDouble


def countPassword(start, end, func):
  count = 0
  for i in range(start, end+1):
    if func(i):
      count += 1
  return count


print('Part 1: ', countPassword(start, end, isPassword))
print('Part 2: ', countPassword(start, end, isPassword2))
