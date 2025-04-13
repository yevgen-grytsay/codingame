package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1000000), 1000000)
	var inputs []string

	var N int
	scanner.Scan()
	fmt.Sscan(scanner.Text(), &N)

	for i := 0; i < N; i++ {
		scanner.Scan()
		inputs = strings.Split(scanner.Text(), " ")
		for j := 0; j < N; j++ {
			elevation, _ := strconv.ParseInt(inputs[j], 10, 32)
			_ = elevation
		}
	}

	// fmt.Fprintln(os.Stderr, "Debug messages...")
	fmt.Println("maybe") // Write answer to stdout
}
