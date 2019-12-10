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
    x, y = i%M, i//N
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
