f = open('d01.in', 'r')

def calculateFuel(mass):
  return mass//3 - 2

def calculateFuelTotal(mass):
  fuel = calculateFuel(mass)
  addition_mass = fuel
  while True:
    addition_mass = addition_mass//3 - 2
    if addition_mass <= 0:
      break
    fuel += addition_mass
  return fuel

fuel1, fuel2 = 0, 0
for mass in map(int, f.read().strip().split('\n')):
  fuel1 += calculateFuel(mass)
  fuel2 += calculateFuelTotal(mass)
print("Puzzle 1: ", fuel1)
print("Puzzle 2: ", fuel2)
