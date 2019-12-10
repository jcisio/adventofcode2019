f = open('d10.in', 'r')
amap = [list(line.strip()) for line in f.read().strip().split('\n')]

def hasObstacles(o1, o2):
    dx, dy = abs(o1[0] - o2[0]), abs(o1[1]-o2[1])
    steps = max(dx, dy)
    if not steps:
        return True
    for i in range(1, steps):
        x = o1[0] + (o2[0] - o1[0])/steps*i
        y = o1[1] + (o2[1] - o1[1])/steps*i
        if x == int(x) and y == int(y) and (x,y) in objects:
            return True
    return False

objects = []
M, N = len(amap[0]), len(amap)
for i in range(M*N):
    x, y = i%M, i//M
    if amap[y][x] == '#':
        objects.append((x,y))

lines_of_sight = []
degrees = [0]*len(objects)
for i in range(len(objects) - 1):
    for j in range(i+1, len(objects)):
        if (hasObstacles(objects[i], objects[j])):
            lines_of_sight.append((objects[i], objects[j]))
            lines_of_sight.append((objects[j], objects[j]))
        else:
            degrees[i] += 1
            degrees[j] += 1

print('Part 1:', max(degrees))

station = objects[degrees.index(max(degrees))]
shots = {}
import math
for o in objects:
    if o == station:
        continue
    dx = o[0] - station[0]
    dy = o[1] - station[1]
    angle = math.atan2(-dx, dy)*180/math.pi
    # Up is 0 degree, convert to that system.
    angle += 180
    if angle >= 360:
        angle -= 360
    if not angle in shots:
        shots[angle] = {}
    shots[angle][o] = dx*dx + dy*dy

n_current = 0
n_stop = 200
while True:
    for i in sorted(shots.keys()):
        n_current += 1
        dmin = M*M+N*N
        for k in shots[i]:
            if shots[i][k] < dmin:
                dmin = shots[i][k]
                current_object = k
        del shots[i][current_object]
        if not shots[i]:
            del shots[i]
        if n_current == n_stop:
            break
    else:
        if not shots:
            break
        continue
    break

if n_current == n_stop:
    print('Part 2:', current_object[0]*100+current_object[1])