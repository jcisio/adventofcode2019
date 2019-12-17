# Day 16 is quite interesting

The first part is, as usual, straightaway. I pre-generate a pattern list of list to reuse it 100 times. However it is noticeable slow. It is not viable to solve the second part using the same algorithm. Actually, the input size is 650, thus the input message length `L = 6.5*10^6`, the pattern list would have a size of `L*L*sizeof(int)`, and I got OOM (out of memory) killed because it requires not less than 100 TB of memory.

I then notice the pattern is easily constructed (`patterns[j]` is the multipliers to calculate the `j`th digits : `output[j] = sum([input[k]*patterns[j][k] for k in range(L)])`)

```
base = [0, 1, 0, -1]
patterns[j][k] = base[(k+1)%(4*(j+1))//(j+1)]
```

Without a pre-generated patterns list, my algorithm is much slower for part 1 (with CPython: 7s instead of 3s, and with PyPy it is 1.3s vs 0.3s because we lost the list here).

With this algorithm, I can do part 2 with `input*10` (so L = 6500) but not with `input*10000`.

## Looking for a fast algorithm

The Flawed Frequency Transmission, when we relate to its acronym FFT (Fast Fourrier Transformation), should be fast. Thus I try to look for some pattern. Let `d(N)` the output after `N` phases, and we can defer the modulo 10 at the end if the sum is always positive.
```
d(N,-1) = d(0,-1)
d(N,-2) = d(0,-2) + d(0,-1)*N
d(N,-3) = d(N-1,-3) + d(N-1,-2) + d(N-1,-1)
        = d(N-1,-3) + [d(0,-2) + (N-1)*d(0,-1)] + d(0,-1)
        = d(N-1,-3) + d(0,-2) + N*d(0,-1)
        = [d(N-2,-3) + d(N-2,-2) + d(N-2,-1)] + d(0,-2) + N*d(0,-1)
        = d(N-2,-3) + [d(0,-2) + (N-2)*d(0,-1)] + d(0,-1) + d(0,-2) + N*d(0,-1)
        = d(N-2,-3) + 2*d(0,-2) + (2N-1)*d(0,-1)
        = [d(N-3,-3) + d(N-3,-2) + d(N-3,-1)] + 2*d(0,-2) + (2N-1)*d(0,-1)
        = d(N-3,-3) + [d(0,-2) + (N-3)*d(0,-1)] + d(N-3,-1)] + 2*d(0,-2) + (2N-1)*d(0,-1)
        = d(N-3,-3) + 3*d(0,-2) + (3N-3)*d(0,-1)
        = d(N-4,-3) + 4*d(0,-2) + (4N-6)*d(0,-1)
        = d(0,-3) + N*d(0,-2) + (N^2-(1+2+...+N-1))*d(0,-1)
        = d(0,-3) + N*d(0,-2) + N*(N+1)/2*d(0,-1)
```

But what next?