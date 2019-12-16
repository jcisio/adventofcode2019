import sys, collections, time

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
    for y in range(y1,y2+1):
        for x in range(x1,x2+1):
            if (x,y) in area:
                c = '⬜️' if area[(x,y)] == TYPE_EMPTY else '⬛️'
                if (x,y)==center:
                    c = 'xx'
                elif area[(x,y)] == TYPE_OXYGEN:
                    c = 'oo'
            else:
                c = '  '
            print(c, end='')
        print()

p_oxygen = None
while remains:
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
            p_oxygen = dst
        remains.append(dst)
    else:
        continue
    break

print('Part 1', len(path[p_oxygen]))

drawarea()

# Part 2: fill from oxygen point.
needed = [x for x in area if area[x] != TYPE_WALL]
filled = collections.deque()
remains.append(p_oxygen)
filled.append(p_oxygen)
step = 0
while len(filled) < len(needed):
    step += 1
    borders = []
    for p in remains:
        for m in moves:
            dst = getDestination(p, m)
            if (dst not in filled) and (dst in area) and (area[dst] != TYPE_WALL):
                borders.append(dst)
                filled.append(dst)
                print('\33[2J')
                area[dst] = TYPE_OXYGEN
                drawarea()
                print(f'Step {step}: {len(filled)}/{len(needed)} remaining')
                sys.stdout.flush()
                time.sleep(0.1)
    remains = collections.deque(borders)
print('Part 2', step)