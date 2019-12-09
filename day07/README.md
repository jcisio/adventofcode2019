# Solve the Day 7 puzzle in Go

**This file contains a lot of off topic stuffs. Be warned!**

This is the first day since my decision to use another language than Python, and I chose a language that I've never used before. It took me about 4 or 5 hours to solve the two parts of this puzzle.

I also checked the [stats](https://adventofcode.com/2019/stats) first. It was about 7.30am CET, only 1h30 after the 7th day, but there were already more than 1000 who finished the two parts. It was also the first time I checked the site that soon: I was on a weekend. Another signal is there were much more, in comparison to the previous days, who only finished the first part. "It would be a funny day", I said to myself.

## Part 1

I started with refactoring Day 5 solution so that I could have a standalone *intCode* that I can call from any language. This part was done quite quickly, even I had to make some research to call that script (written in Python, because I changed very little to make standalone script) in... Python. I had to make sure that my script worked as expected. Looking back now, I could have rewritten the main script in another language (e.g. Bash) because it has only 4 lines:

```python
from subprocess import run, PIPE
values = open('d05.in', 'r').read()
print('Part 1: ', run('python3 d05-intCode.py'.split(), text=True, input=values+'1', stdout=PIPE).stdout.strip())
print('Part 2: ', run('python3 d05-intCode.py'.split(), text=True, input=values+'5', stdout=PIPE).stdout.strip())
```

Well, back to the topic: the Day 7 puzzle. Part 1 is quite trivial: let the *intCode* runs on all permutations of `01234` and return the maximum result. Generating all permutations is just a few lines in any languages (even if I used Python, it would be *one* line thanks to the *itertools* module). Running an external program and intercepting stdin/stdout is also must have feature in any modern language (maybe not true for JavaScript, because I would have to set up a native messaging host, in Chrome, something I don't want to invest my time into). All that said, using any language is ok with today puzzle, as there won't be many lines of code. I decided then to use Go, a language that I have never written a single line of code.

First, install Go. Then copy/paste the permutation code from the [first page](https://yourbasic.org/golang/generate-permutation-slice-string/) I found on Google. I needed to save time because there will certainly be bugs in the code I would write. Here it come the code I write: run an external program in Go. I spent about an hour on it.

```Go
func runIntCode(code, input string) string {
	cmd := exec.Command("python3", "../day05/d05-intCode.py")
	cmd.Stdin = strings.NewReader(code + "\n" + input)
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Run()
	return strings.TrimSpace(out.String())
}
```

I then need another helper function, to take a permutation of `01234`, run the five amplifiers and take the result. This part is trivial, even in the first versions there were also `programmeCode` and `input` in the function signature. But it turned out that global variables work well, and it saved time.

```Go
func runAcs(phase string) string {
	input := "0"
	for _, p := range phase {
		output := runIntCode(programCode, input+","+string(p))
		input = output
	}
	return input
}
```

Now the algorithm. Just run this program with any permutation of `01234` and return the max result. The permutation generator code that I copied already has a callback that I can use.

```Go
func perm(a string, f func(phase string) string, i int) {
	if i > len(a) {
        // BEGIN
		result, _ := strconv.Atoi(f(string(a)))
		if result > maxThruster {
			maxPhase = string(a)
			maxThruster = result
        }
        // END
		return
	}
	perm(a, f, i+1)
	b := []rune(a)
	for j := i + 1; j < len(b); j++ {
		b[i], b[j] = b[j], b[i]
		perm(string(b), f, i+1)
		b[i], b[j] = b[j], b[i]
	}
}
```

I modified the `BEGIN...END` block to insert the logic. And it's done with `perm("01234", runAcs, 0)`. It took 6 seconds to finish because it create sub process to call external program (which is slow, because the Python interpreter must run first). I started to be afraid of it not being fast enough for part 2. However, I got the correct result for part 1 in my first try, it was a good point already.

## Part 2

Now I have to managed the state of each amplifier. How to do that, without using Python, or porting intCode to Go, of course? My first attempt is to use a special extra input to tell intCode where to start, so that it know where to continue in the next loop. I didn't got the correct answer. It turned out that I had to keep the full state, because the `programmeCode` is changed during a run.

During my first attempt, I noticed that the amplifiers always return the same sub output in each loop. Then I figured out instead of sending one input in the next loop at a specific position, I could simply send the old inputs, plus the new one, and ask intCode to run from the beginning everytime. It worked! I no longer saw the repeated output in my first attempt. The result was not correct though. It were much smaller than the expected result. It seemed that intCode stoped early.

I checked a few places, checked which amplifier stop first and how to handled the others, but the bug was not there. Then I spent more time on Reddit, where some brillant user made a [real intCode machine in a terminal](https://www.reddit.com/r/adventofcode/comments/e7g3ju/intcode_computer_in_your_terminal_link_in_the/). It was interesting, but I didn't help me. Another user post a list of specific remarks in the puzzle, but I already got them right.

In another attempt, I keep the machine going. I indeed got an error: an `IndexError` exception because I called `input.pop()` where `input` was empty. To trace the error, I let the machine display input/output state in each instruction and I got what I wanted: since the input is empty, I got one more output before the error appear. The bug is figured out. I wrote something like this at the end of each instruction:

```Python
  if  HaltOnFirstOutput and not input and output:
    break
```

I did not pay attention to the fact that output is written with instruction `4`, it does not need input. Checking non empty output was not useful, because output is always non empty from the 3rd input (i.e. since the second iteration of the amplifiers feedback, when amp 1 gets the input from amp 5). I rewrote the code:

```Python
  while True:
    # ...
    elif instruction == 3:
      if not input:
        break
      values[values[i+1]] = input.pop()
    # ...
    if  HaltOnFirstOutput:
      output = output[numInputs-2:]
```
Two changes: we halt just before instruction 3 on empty array, and we return the last element of output. I don't write `output = output[-1]` because I want to return empty output when intCode goes over the instruction 99, when it is fed with more input than necessary.

And it worked!

## Performance

`d05.py` takes 57 ms to finish. `d07.go` takes 80 s on the same PC (Thinkpad x280 with i5-8250U) for two parts, and 76 s for part 2 only. ~~It runs on 24 iterations, or `24*5 = 120` times the intCode machine. 630 ms in average to run the intCode, it is fairly slow~~.

To compare apples to apples, I reuse the code to solve Day 5 with Go, it is only a few lines:

```Go
	data, _ := ioutil.ReadFile("../day05/d05.in")
	programCode = strings.TrimSpace(string(data))
	fmt.Printf("Part 1: %s\n", runIntCode(programCode, "1"))
	fmt.Printf("Part 2: %s\n", runIntCode(programCode, "5"))
}
```

I got 250 ms comparing to 57 ms with Python. So Go does have some extra overhead running external program. As I am a complete novice in Go, I won't go further for now.

> **Update:** 120 is the number of permutations (`5!`) of `01234`, but for each permutation there are many iterations of 5 amplifiers, so the above calculation was wrong. I ran quickly `d07.go` again and measured 6720 calls of `runIntCode`, so actually it takes about 10 ms to run each intCode machine. Maybe Go is as fast as Python if the compilation time is taken into account. Compilation time overhead of Go is (non scientifically measured) 230 ms using my PC.

One more thing: we don't care much about performance here, as we only need the result. However, if we needed to run *intCode* millions of times, there should be a way to *import* the Python module and use it, instead of running an external command. Another possiblity is to run intCode *as-a-service*, the overhead should be much less, even it is more than an imported module.