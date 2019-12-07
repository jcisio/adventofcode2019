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
var maxThruster int = 0

func perm(a string, i int) {
	if i > len(a) {
		result, _ := strconv.Atoi(runAcs(programCode, string(a), input))
		if result > maxThruster {
			maxPhase = string(a)
			maxThruster = result
		}
		return
	}
	perm(a, i+1)
	b := []rune(a)
	for j := i + 1; j < len(b); j++ {
		b[i], b[j] = b[j], b[i]
		perm(string(b), i+1)
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

func runAcs(code, phase, input string) string {
	for _, p := range phase {
		output := runIntCode(code, input+","+string(p))
		input = output
	}
	return input
}

func main() {
	data, err := ioutil.ReadFile("d07.in")
	if err != nil {
		panic(err)
	}
	programCode = string(data)
	print(data)
	input = "0"
	perm("01234", 0)
	fmt.Printf("Part 1: %d\n", maxThruster)
}
