import sys

N_REPEAT = 10000
N_ITERATION = 100

with open('d16.in') as f:
    input = f.read().strip()

def get_output(input, iterations):
    L = len(input)
    base = [0, 1, 0, -1]
    input = list(map(int, input))
    for i in range(iterations):
        input = [abs(sum([input[k]*base[(k+1)%(4*(j+1))//(j+1)] for k in range(L)])) % 10 for j in range(L)]
    return ''.join(map(str, input))

#print('Part 1:', get_output(input, N_ITERATION)[0:8])

L = len(input)*N_REPEAT
offset = int(input[0:7])
if (offset < L/2):
    sys.exit('Oh my, I have no idea deal with that offset.')

input = input*N_REPEAT
output = []
for i in range(offset, offset+8):
    c = int(input[i])
    coeff = 1
    for j in range(i+1,L):
        coeff = coeff*(N_ITERATION+j-i-1)//(j-i)
        c += int(input[j])*coeff
    output.append(c % 10)
print('Part 2:', ''.join(map(str, output)))