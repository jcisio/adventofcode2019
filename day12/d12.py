import re

moon = [list(map(int, re.search('<x=(.*), y=(.*), z=(.*)>', line).groups())) + [0]*3 for line in open('d12.in').read().strip().split('\n')]

def move():
    for m1 in moon:
        for m2 in moon:
            for i in range(3):
                axe = i+3
                if m1[i]==m2[i]: continue
                if m1[i] < m2[i]:
                    m1[i+3] += 1
                    m2[i+3] -= 1
    for m in moon:
        for i in range(3):
            m[i] += m[i+3]

def energy(m):
    return sum([abs(m[i]) for i in range(3)])*sum([abs(m[i]) for i in range(3,6)])


for i in range(1000):
    move()


print('Part 1:', sum([energy(m) for m in moon]))