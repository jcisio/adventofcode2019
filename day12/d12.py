import re
import copy

moon = [list(map(int, re.search('<x=(.*), y=(.*), z=(.*)>', line).groups())) + [0]*3 for line in open('d12.in').read().strip().split('\n')]
step = 0
def move():
    global step
    step += 1
    # Velocity
    for m1 in moon:
        for m2 in moon:
            for i in range(3):
                if m1[i]==m2[i]: continue
                if m1[i] < m2[i]:
                    m1[i+3] += 1
                    m2[i+3] -= 1
    # Position
    for m in moon:
        for i in range(3):
            m[i] += m[i+3]
    for i in range(3):
        if not steps[i] and get_state(i) == init[i]:
            steps[i] = step

def energy(m):
    return sum([abs(m[i]) for i in range(3)])*sum([abs(m[i]) for i in range(3,6)])

def get_state(axe):
    state = [(m[axe], m[axe+3]) for m in moon]
    return state

def gcd(a, b):
    if a > b:
        a, b = b, a
    if a == 0:
        return b
    return gcd(b%a, a)

def lcm(a, b):
    return a*b//gcd(a,b)

init = [get_state(i) for i in range(3)]
steps = [0]*3

for i in range(1000):
    move()
print('Part 1:', sum([energy(m) for m in moon]))


for i in range(1000000):
    move()
    if 0 not in steps:
        break
print('Part 2:', lcm(steps[0],lcm(steps[1],steps[2])))