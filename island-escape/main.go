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

	board := Board{
		width:  N,
		height: N,
		grid:   make([][]Cell, N),
	}

	for i := 0; i < N; i++ {
		board.grid[i] = make([]Cell, N)
		scanner.Scan()
		inputs = strings.Split(scanner.Text(), " ")
		for j := 0; j < N; j++ {
			elevation, _ := strconv.ParseInt(inputs[j], 10, 32)
			fmt.Fprint(os.Stderr, fmt.Sprintf("%d ", elevation))
			// _ = elevation
			board.grid[i][j] = Cell{
				row:   i,
				col:   j,
				index: i*N + j,
				value: int(elevation),
			}
		}
		fmt.Fprint(os.Stderr, "\n")
	}

	// fmt.Fprintln(os.Stderr, "Debug messages...")
	// fmt.Println("maybe") // Write answer to stdout
	fmt.Println(board.findSolution(N/2, N/2)) // Write answer to stdout
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

func (b Board) getAdjacent(row int, col int, value int) []Cell {
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
			cell := b.grid[index.i][index.j]
			if cell.value == value || cell.value == (value-1) || cell.value == (value+1) {
				result = append(result, cell)
			}
		}
	}

	return result
}

func (b Board) findSolution(i int, j int) string {
	root := b.grid[i][j]

	var q []Cell = []Cell{root}
	var visited map[int]bool = map[int]bool{
		root.index: true,
	}

	for len(q) > 0 {
		current := q[0]
		q = q[1:]
		value := current.value
		adjacent := b.getAdjacent(current.row, current.col, value)

		for _, ad := range adjacent {
			if _, ok := visited[ad.index]; ok {
				continue
			}

			visited[ad.index] = true

			if ad.value == 0 {
				return "yes"
			}

			q = append(q, ad)
		}
	}

	return "no"
}
