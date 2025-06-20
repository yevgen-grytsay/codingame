package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 * NOTE:
 * In the default code, a single prize is read before the
 * rest are read in a loop due to a current limitation in
 * stub generation. The number of prizes is (1 + height)
 **/

type Board struct {
	rows   [][]int
	prizes []int
}

func (b *Board) ParseAndAddRow(row string) {
	expectedLength := len(b.rows) + 1
	if len(row) != expectedLength {
		panic(fmt.Errorf("expected lenght of a new row is %d, but actual is %d", expectedLength, len(row)))
	}

	list := strings.Split(row, "")
	var newRow []int

	for _, s := range list {
		value, _ := strconv.Atoi(s)
		newRow = append(newRow, value)
	}

	b.rows = append(b.rows, newRow)
}

func (b *Board) SetPrizes(prizes []int) {
	b.prizes = prizes
}

func (b Board) String() string {
	var parts []string
	for i := 0; i < len(b.rows); i++ {
		parts = append(parts, fmt.Sprintf("%#v", b.rows[i]))
	}

	parts = append(parts, fmt.Sprintf("%#v", b.prizes))

	return strings.Join(parts, "\n")
}

var board = Board{}

func findSum(b Board) int {
	var sums = []int{
		b.rows[0][0],
	}

	sumF := func(a, b int) int {
		return a + b
	}
	mulF := func(a, b int) int {
		return a * b
	}

	op := sumF

	rows := append(b.rows[1:], b.prizes)

	var newSums []int

	for i, row := range rows {
		if i == (len(rows) - 1) {
			op = mulF
		} else {
			op = sumF
		}

		newSums = make([]int, len(row))
		var lastIndex = len(row) - 1

		for col, mul := range row {
			var a, b int
			var isFirstCol = col == 0
			var isLastCol = col == lastIndex

			if !isFirstCol {
				a = op(sums[col-1], mul)
			}

			if !isLastCol {
				b = op(sums[col], mul)
			}

			newSums[col] = maxInt(a, b)
		}

		sums = newSums
	}

	return maxInx2(newSums...)
}

func maxInt(a, b int) int {
	return int(math.Max(float64(a), float64(b)))
}

func maxInx2(values ...int) int {
	var max = math.MinInt
	for _, val := range values {
		if val > max {
			max = val
		}
	}

	return max
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1000000), 1000000)

	var height int
	scanner.Scan()
	fmt.Sscan(scanner.Text(), &height)

	for i := 0; i < height; i++ {
		scanner.Scan()
		increments := scanner.Text()
		board.ParseAndAddRow(increments)
	}

	var totalPrizes = make([]int, height+1)
	for i := 0; i <= height; i++ {
		var prize int
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &prize)
		totalPrizes[i] = prize
	}

	board.SetPrizes(totalPrizes)

	fmt.Fprintln(os.Stderr, board)

	fmt.Println(findSum(board)) // Write answer to stdout
}
