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

But what next? I was in a train and my train arrived soon to London, so I stopped there but I already had an idea before I wrote down the lines above. I noticed the triangle of 1 from the bottom and I did enough combinatorics in highschool to relate it to Pascal's triangle. Thus I tried to find the coefficients in the form of binomial coefficients. And I ran out of time.

Then I continued at night. I still haven't figured out the coefficients, but it's something I could manage to do, so I left it as is, because there is another problem: only the half bottom rows have simplified formula. Effectively, at row L/2, the pattern is L/2 0s and L/2 1s, so it ends as an array of 1. But if we go up, there are now 0 and -1 that breaks our triangle. I stuck there for more than half an hour, then I decided to go to the subreddit: many Day 17 topics (I was one day late), and few Day 16. But it was enough: I read a hint that the message is actually in the second half of the string, so we only have to take care of our triangle of 1s. It was something I hadn't imagine, because I thought the the offset was there to have double roles:

- I had to decode the first 7 digits (I wrongly thought the offset is from the decoded message, but it turned out to be from the initial message).
- Then I had to decode any random digits because of the offset.

In other words, I thought I had to decode the whole message. How inexperienced was I!

Now I got all the details, the remain is maths. From the above steps, I guess that `d(N,-3) = d(0,-3) + C(N,1)*d(0,-2) + C(N+1,2)*d(0,-1)`. Then for `d(N,-4)`:
```
d(N,-4) = d(N-1,-4) + d(N-1,-3) + d(N-1,-2) + d(N-1,-1)
        = d(N-1,-4) + [d(0,-3) + C(N-1,1)*d(0,-2)] + [d(0,-2) + (N-1)*d(0,-1)] + d(0,-1)
        = d(N-1,-4) + d(0,-3) + C(N,1)*d(0,-2) + C(N,1)*d(0,-1)
```

Now we write them all down to find a pattern:
```
d(N,-1) = d(0,-1)
d(N,-2) = d(0,-2) + C(N,1)d(0,-1)
d(N,-3) = d(0,-3) + C(N,1)d(0,-2) + C(N+1,2)d(0,-1)
d(N,-4) = d(0,-4) + C(N,1)d(0,-3) + C(N+1,2)d(0,-2) + C(N+2,3)d(0,-1) ?
```
Using induction:
```
d(N-1,-4) = d(0,-4) + C(N-1,1)d(0,-3) + C(N,2)d(0,-2) + C(N+1,3)d(0,-1) (hypothesis)
d(N,-4) = d(N-1,-4) + d(N-1,-3) + d(N-1,-2) + d(N-1,-1)
        = d(0,-4) + C(N-1,1)d(0,-3) + C(N,2)d(0,-2) + C(N+1,3)d(0,-1)
        + d(0,-3) + C(N-1,1)*d(0,-2) + C(N,2)*d(0,-1)
        + d(0,-2) + C(N-1,1)d(0,-1)
        + d(0,-1)
        = d(0,-4) + C(N,1)d(0,-3) + C(N+1,2)d(0,-2) + C(N+2,3)d(0,-1)
```
It's good. Now `d(N,-5)`:
```
d(N-1,-5) = d(0,-5) + C(N-1,1)d(0,-4) + C(N,2)d(0,-3) + C(N+1,3)d(0-2) + C(N+2,4)d(0,-1) (hypothesis)
d(N,-5) = d(N-1,-5) + d(N-1,-4) + d(N-1,-3) + d(N-1,-2) + d(N-1,-1)
        = d(0,-5) + C(N-1,1)d(0,-4) + C(N,2)d(0,-3) + C(N+1,3)d(0,-2) + C(N+2,4)d(0,-1)
        + d(0,-4) + C(N-1,1)d(0,-3) + C(N,2)d(0,-2) + C(N+1,3)d(0,-1)
        + d(0,-3) + C(N-1,1)d(0,-2) + C(N,2)d(0,-1)
        + d(0,-2) + C(N-1,1)d(0,-1)
        + d(0,-1)
        = d(0,-5) + C(N,1)d(0,-4) + C(N+1,2)d(0,-3) + X*d(0,-2) + Y*d(0,-1)
X = C(N+1,3) + C(N,2) + C(N-1,1) + 1
  = (N+1)(N-1)N/6 + N(N-1)/2 + N-1 + 1
  = N((N-1)(N+1) + 3(N-1) + 6)
  = N(N^2 + 3N + 2)/6
  = N(N+1)(N+2)/6
  = C(N+2,3)
Y = C(N+2,4) + C(N+1,3) + C(N,2) + C(N-1,1) + 1
  = (N+2)(N+1)N(N-1)/24 + (N+1)N(N-1)/6 + N(N-1)/2 + N
  = N((N+2)(N-1)(N+1) + (N-1)(N+1)*4 + (N-1)*12 + 24)/24
  = N(N+1)((N+2)(N-1) + 4(N-1) + 12)/24
  = N(N+1)(N^2+N-2 + 4N-4 + 12)/24
  = N(N+1)(N^2 + 5N + 6)/24
  = N(N+1)(N+2)(N+3)/24
  = C(N+3,4)
=> d(N,-5) = d(0,-5) + C(N,1)d(0,-4) + C(N+1,2)d(0,-3) + C(N+2,3)d(0,-2) + C(N+3,4)d(0,-1)
```
A lot of basic manipulation. When I was doing that, I got another idea to avoid all of that. But because I have "unlimited" time, I'll explore that idea later.

It's time to implement this algorithm in Python. I even don't need to find a module to calculate binomial coefficient in Python, because I can calculate them fast from one coefficient to another. I won't write the detail here, I'll write it directly in Python.
```python
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
```
And bingo, "That's the right answer!" However it is much slower than I think to calculate just 8 digits. CPython take 4.7s for part 2, and PyPy 3.6s. It is because the coefficient is quite big: 262 digits. Is there any faster method?

## Without maths

As I said above, I had another idea when I was doing the expansion. No maths at all, just compute. ~~In the worst case, we will do -`L/2*100*8 = 2.6*10^9`- additions~~. It is much doable.

It took me like 5 minutes to write this:
```python
    input = list(map(int, (input*N_REPEAT)[offset:]))
    output = input.copy()
    for i in range(N_ITERATION):
        for j in range(len(input)):
            output[j] = sum(input[j:]) % 10
        input = output.copy()
    return ''.join(map(str, output))
```
And it takes forever trying to finish the first iteration. When I look at the code, the complexity analyse above is wrong, it actually needs `100*(L/2)^2 = 10^15` additions to finish.

Lesson learnt: *sometimes we can just let the computer do the computing, but sometimes maths is helpful to solve impossible computing problem*.

PS: now I got two stars, I went take a look on subreddit, and found that my method above is far from optimized. Each iteration could be written as:
```python
    for _ in range(N_ITERATION):
        output[-1] = input[-1]
        for j in range(L2-2, -1, -1):
            output[j] = (output[j+1] + input[j]) % 10
        input = output.copy()
```
We reduced the complexity of each iteration from O(L^2) to O(L), and PyPy finished in 0.57s instead of 3.6s (but CPython is slower: 6.4s). We can see this trick is many place, to do sub array sum in O(1) (with O(L) preparation time) instead of O(L) without preparation.

A user, bla2, cleverly [remarked](https://www.reddit.com/r/adventofcode/comments/ebxz7f/2019_day_16_part_2_visualization_and_hardmode/) that we can apply this trick to calculate the full message. The complexity per iteration is now O(LlogL) instead of O(L). With `L = 6.5*10^6` and 100 iteration, Python will be two slow and his C implementation finished in 50s.