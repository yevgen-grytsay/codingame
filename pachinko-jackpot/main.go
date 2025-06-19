package main

import (
	"bufio"
	"fmt"
	"os"
)

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 * NOTE:
 * In the default code, a single prize is read before the
 * rest are read in a loop due to a current limitation in
 * stub generation. The number of prizes is (1 + height)
 **/

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1000000), 1000000)

	var height int
	scanner.Scan()
	fmt.Sscan(scanner.Text(), &height)

	for i := 0; i < height; i++ {
		scanner.Scan()
		increments := scanner.Text()
		_ = increments // to avoid unused error
	}
	var prize1 int
	scanner.Scan()
	fmt.Sscan(scanner.Text(), &prize1)
	for i := 0; i < height; i++ {
		var prize int
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &prize)
	}

	// fmt.Fprintln(os.Stderr, "Debug messages...")
	fmt.Println("jackpot") // Write answer to stdout
}
