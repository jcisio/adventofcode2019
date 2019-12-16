import sys, collections

sys.path.append('../common')
import intcode

TYPE_WALL = 0
TYPE_EMPTY = 1
TYPE_OXYGEN = 2

moves = {
    1: (0, -1),
    2: (0, 1),
    3: (-1, 0),
    4: (1, 0),
}


with open('d15.in') as f:
    values = list(map(int, f.read().strip().split(',')))

intcode.init(values)
center = (0,0)
area = {center: TYPE_EMPTY}
path = {center: []} # path from (0,0)
remains = collections.deque()
remains.append(center)

def getDestination(p, m):
    return (p[0]+moves[m][0], p[1]+moves[m][1])


def drawarea():
    x1 = min([p[0] for p in area])
    x2 = max([p[0] for p in area])
    y1 = min([p[1] for p in area])
    y2 = max([p[1] for p in area])
    for x in range(x1,x2+1):
        for y in range(y1,y2+1):
            if (x,y)==center:
                c = 'x'
            elif (x,y) in area:
                c = area[(x,y)]
            else:
                c = '?'
            print(c, end='')
        print()

while True:
    if not remains:
        break
    p = remains.popleft()
    for m in moves:
        dst = getDestination(p, m)
        if dst in path:
            continue
        intcode.init(values)
        path[dst] = path[p] + [m]
        area[dst] = intcode.runIntCode(path[dst].copy())[-1]
        if area[dst]==TYPE_WALL:
            continue
        if area[dst]==TYPE_OXYGEN:
            break
        remains.append(dst)
    else:
        continue
    break

print('Part 1', len(path[dst]))