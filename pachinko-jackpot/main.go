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

func (b Board) GetHeight() int {
	return len(b.rows)
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

func (b Board) GetRootNode() Node {
	return Node{
		row:   0,
		col:   0,
		value: b.rows[0][0],
	}
}

func (b Board) GetNeighbors(node Node) (Node, Node) {
	nextRowIndex := node.row + 1
	if nextRowIndex >= len(b.rows) {
		panic(fmt.Sprintf("invalid row index %d (total rows: %d)", nextRowIndex, len(b.rows)))
	}

	return Node{row: nextRowIndex, col: node.col, value: b.rows[nextRowIndex][node.col]},
		Node{row: nextRowIndex, col: node.col + 1, value: b.rows[nextRowIndex][node.col+1]}
}

type Node struct {
	row   int
	col   int
	value int
}

var board = Board{}

func findSum2(b Board) int {
	var sums = []int{
		b.GetRootNode().value,
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
		// var lastSum = sums[len(sums)-1]
		// newSums[0] = sums[0] + row[0]
		// newSums[lastIndex] = lastSum + row[lastIndex]

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

func findSum(b Board, multiplier int, node Node) int {
	maxRowIndex := b.GetHeight() - 1
	if node.row == maxRowIndex {
		prizeA := b.prizes[node.col]
		prizeB := b.prizes[node.col+1]

		return multiplier * maxInt(prizeA, prizeB)
	}

	nodeA, nodeB := b.GetNeighbors(node)

	sumA := findSum(b, multiplier+nodeA.value, nodeA)
	sumB := findSum(b, multiplier+nodeB.value, nodeB)

	return maxInt(sumA, sumB)
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
		// _ = increments // to avoid unused error
	}
	// var prize1 int
	// scanner.Scan()
	// fmt.Sscan(scanner.Text(), &prize1)
	var totalPrizes = make([]int, height+1)
	for i := 0; i <= height; i++ {
		var prize int
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &prize)
		totalPrizes[i] = prize
	}

	board.SetPrizes(totalPrizes)

	fmt.Fprintln(os.Stderr, board)
	// fmt.Println("jackpot") // Write answer to stdout

	// rootNode := board.GetRootNode()
	// fmt.Println(findSum(board, rootNode.value, rootNode)) // Write answer to stdout
	fmt.Println(findSum2(board)) // Write answer to stdout
}
