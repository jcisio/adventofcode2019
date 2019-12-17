with open('d16.in') as f:
    input = f.read().strip()

def get_output(input, iterations):
    L = len(input)
    base = [0, 1, 0, -1]
    input = list(map(int, input))
    for i in range(iterations):
        input = [abs(sum([input[k]*base[(k+1)%(4*(j+1))//(j+1)] for k in range(L)])) % 10 for j in range(L)]
    return ''.join(map(str, input))

print('Part 1:', get_output(input, 100)[0:8])

input='03036732577212944063491565474664'
input_p2 = input*10000
ouput_p2 = get_output(input_p2, 100)
offset = int(ouput_p2[0:7])
print(ouput_p2[offset:offset+8])