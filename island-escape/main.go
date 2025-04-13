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

type Cell struct {
	value int
	index int
	row   int
	col   int
}

type Board struct {
	width  int
	height int
	grid   [][]Cell
}

func (b Board) getAdjacent(row int, col int) []Cell {
	indices := []struct {
		i int
		j int
	}{
		{row - 1, col},
		{row, col - 1},
		{row, col + 1},
		{row + 1, col},
	}

	var result []Cell
	for _, index := range indices {
		if index.i >= 0 && index.i < b.height && index.j >= 0 && index.j < b.width {
			result = append(result, b.grid[index.i][index.j])
		}
	}

	return result
}
