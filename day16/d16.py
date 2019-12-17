with open('d16.in') as f:
    input = f.read().strip()

def get_output(input, iterations):
    L = len(input)
    patterns = []
    for i in range(1, L+1):
        base = [0]*i + [1]*i +  [0]*i + [-1]*i
        pattern = base.copy()[1:]
        while len(pattern) < L:
            pattern += base.copy()
        patterns.append(pattern[:L])
    input = list(map(int, input))
    for i in range(iterations):
        input = [abs(sum([input[k]*patterns[j][k] for k in range(L)])) % 10 for j in range(L)]
    return ''.join(map(str, input))

print('Part 1:', get_output(input, 100)[0:8])