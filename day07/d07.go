package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os/exec"
	"strconv"
	"strings"
)

var programCode, input string
var maxPhase string
var maxThruster int

func perm(a string, f func(phase string) string, i int) {
	if i > len(a) {
		result, _ := strconv.Atoi(f(string(a)))
		if result > maxThruster {
			maxPhase = string(a)
			maxThruster = result
		}
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

func runIntCode(code, input string) string {
	cmd := exec.Command("python3", "../day05/d05-intCode.py")
	cmd.Stdin = strings.NewReader(code + "\n" + input)
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Run()
	return strings.TrimSpace(out.String())
}

func runAcs(phase string) string {
	input := "0"
	for _, p := range phase {
		output := runIntCode(programCode, input+","+string(p))
		input = output
	}
	return input
}

func runAcs2(phase string) string {
	var machineOutputs [5][]string

	for i, p := range phase {
		machineOutputs[i] = append(machineOutputs[i], string(p), "HaltOnFirstOutput")
	}
	machineOutputs[0] = append([]string{"0"}, machineOutputs[0]...)
	for i := 0; ; i++ {
		output := runIntCode(programCode, strings.Join(machineOutputs[i%5], ","))
		// If the same output is detected, it means that there is no new output.
		if output == "" {
			break
		}
		machineOutputs[(i+1)%5] = append([]string{output}, machineOutputs[(i+1)%5]...)

	}
	return machineOutputs[0][0]
}

func day07() {
	data, err := ioutil.ReadFile("d07.in")
	if err != nil {
		panic(err)
	}
	programCode = strings.TrimSpace(string(data))

	maxThruster = 0
	perm("01234", runAcs, 0)
	fmt.Printf("Part 1: %d\n", maxThruster)

	maxThruster = 0
	perm("56789", runAcs2, 0)
	fmt.Printf("Part 2: %d\n", maxThruster)
}

func day05() {
	data, err := ioutil.ReadFile("../day05/d05.in")
	if err != nil {
		panic(err)
	}
	programCode = strings.TrimSpace(string(data))

	fmt.Printf("Part 1: %s\n", runIntCode(programCode, "1"))
	fmt.Printf("Part 2: %s\n", runIntCode(programCode, "5"))
}

func main() {
	day07()
}
