package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1000000), 1000000)

	// N: Number of elements which make up the association table.
	var N int
	scanner.Scan()
	fmt.Sscan(scanner.Text(), &N)

	// Q: Number Q of file names to be analyzed.
	var Q int
	scanner.Scan()
	fmt.Sscan(scanner.Text(), &Q)

	var table map[string]string = make(map[string]string)
	for i := 0; i < N; i++ {
		// EXT: file extension
		// MT: MIME type.
		var EXT, MT string
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &EXT, &MT)
		table[strings.ToLower(EXT)] = MT
	}
	for i := 0; i < Q; i++ {
		scanner.Scan()
		FNAME := scanner.Text()
		_ = FNAME // to avoid unused error // One file name per line.

		fmt.Fprintln(os.Stderr, "debug: "+FNAME)
		var ext string
		lastIndex := strings.LastIndex(FNAME, ".")
		if lastIndex == -1 {
			ext = ""
		} else {
			parts := strings.Split(FNAME, ".")
			ext = strings.ToLower(parts[len(parts)-1])
		}

		mime, ok := table[ext]
		if ok {
			fmt.Println(mime)
		} else {
			fmt.Println("UNKNOWN")
		}
	}

	// fmt.Fprintln(os.Stderr, "Debug messages...")

	// For each of the Q filenames, display on a line the corresponding MIME type. If there is no corresponding type, then display UNKNOWN.
	// fmt.Println("UNKNOWN")
}
