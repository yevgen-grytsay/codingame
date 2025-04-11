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
 **/

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1000000), 1000000)
	var inputs []string

	var depth int
	scanner.Scan()
	fmt.Sscan(scanner.Text(), &depth)

	crawler := NewCrawler(depth)
	state := State{grid: make([]Cell, 9)}

	for i := 0; i < 3; i++ {
		scanner.Scan()
		inputs = strings.Split(scanner.Text(), " ")
		for j := 0; j < 3; j++ {
			value, _ := strconv.ParseInt(inputs[j], 10, 32)
			state.grid[i*3+j] = Cell{index: i*3 + j, value: int(value)}
		}
	}

	fmt.Fprintln(os.Stderr, depth)
	fmt.Fprintln(os.Stderr, state)

	sum := crawler.run(state)

	// fmt.Fprintln(os.Stderr, "Debug messages...")
	fmt.Println(sum) // Write action to stdout
}

type Cell struct {
	index int
	value int
}

type State struct {
	grid []Cell
}

func (s State) getNeighbors(cell Cell) []Cell {
	return s.getNeighbors2(cell.index)
}

func (s State) getNeighbors2(index int) []Cell {
	indices := []int{
		index - 3,
		index - 1,
		index + 1,
		index + 3,
	}

	var result []Cell
	for _, i := range indices {
		if i >= 0 && i < len(s.grid) {
			result = append(result, s.grid[i])
		}
	}

	return result
}

func (s State) getFilledNeighbors(index int) []Cell {
	i := index / 3
	j := index % 3

	var indices [][]int
	if i > 0 {
		indices = append(indices, []int{i - 1, j})
	}

	if i < 2 {
		indices = append(indices, []int{i + 1, j})
	}

	if j > 0 {
		indices = append(indices, []int{i, j - 1})
	}

	if j < 2 {
		indices = append(indices, []int{i, j + 1})
	}

	var result []Cell
	for _, item := range indices {
		i := item[0]*3 + item[1]

		if s.grid[i].value == 0 {
			continue
		}

		result = append(result, s.grid[i])
	}

	return result
}

func (s State) without(index int) State {
	return s.with(index, 0)
}

func (s State) with(index int, value int) State {
	var grid = make([]Cell, 9)
	for i, cell := range s.grid {
		grid[i] = Cell{index: cell.index, value: cell.value}
	}

	grid[index].value = value

	return State{grid: grid}
}

func (s State) hasFreeCells() bool {
	freeCells := s.getFree()

	return len(freeCells) > 0
}

func (s State) getFree() []Cell {
	var result []Cell
	for _, cell := range s.grid {
		if cell.value == 0 {
			result = append(result, cell)
		}
	}

	return result
}

func (s State) hash() int {
	var str string
	for _, cell := range s.grid {
		str += fmt.Sprintf("%d", cell.value)
	}

	number, error := strconv.Atoi(str)
	if error != nil {
		panic(fmt.Sprintf("Can not convert %s to int", str))
	}

	return number
}

func (Cell) New(index int, value int) Cell {
	return Cell{
		index: index,
		value: value,
	}
}

type Crawler struct {
	depth int
	cache map[string]int
}

func NewCrawler(depth int) *Crawler {
	return &Crawler{depth: depth, cache: make(map[string]int)}
}

func (c *Crawler) run(state State) int {
	sum := c.handle(state, c.depth)

	return sum
}

func (c *Crawler) handle(state State, limit int) int {
	if limit == 0 || !state.hasFreeCells() {
		return state.hash()
	}

	cacheKey := fmt.Sprintf("%d_%d", state.hash(), limit)

	value, ok := c.cache[cacheKey]
	if ok {
		return value
	}

	var sum int
	freeCells := state.getFree()
	for _, cell := range freeCells {
		nextStateList := put(state, cell.index)

		for _, nextState := range nextStateList {
			nHash := c.handle(nextState, limit-1)
			sum = (sum + nHash) % int(math.Pow(2, 30))
		}
	}

	c.cache[cacheKey] = sum

	return sum
}

func put(state State, index int) []State {
	neighbors := state.getFilledNeighbors(index)
	if len(neighbors) == 0 {
		return []State{state.with(index, 1)}
	}

	var samples [][]Cell
	samples = append(samples, sample2(neighbors)...)
	samples = append(samples, sample3(neighbors)...)

	if len(neighbors) == 4 && sumCells(neighbors) <= 6 {
		samples = append(samples, neighbors)
	}

	if len(samples) == 0 {
		return []State{state.with(index, 1)}
	}

	var result []State
	for _, sample := range samples {
		newState := state
		for _, cell := range sample {
			newState = newState.without(cell.index)
		}
		newState = newState.with(index, sumCells(sample))
		result = append(result, newState)
	}

	return result
}

func sumCells(list []Cell) int {
	var result int
	for _, cell := range list {
		result += cell.value
	}

	return result
}

func sample2(list []Cell) [][]Cell {
	var result [][]Cell

	if len(list) < 2 {
		return result
	}

	for i := 0; i < (len(list) - 1); i++ {
		if list[i].value == 0 {
			continue
		}
		for j := i + 1; j < len(list); j++ {
			if list[j].value == 0 {
				continue
			}

			if list[i].value+list[j].value <= 6 {
				result = append(result, []Cell{list[i], list[j]})
			}
		}
	}

	return result
}

func sample3(list []Cell) [][]Cell {
	var result [][]Cell

	if len(list) < 3 {
		return result
	}

	for i := 0; i < (len(list) - 2); i++ {
		if list[i].value == 0 {
			continue
		}
		for j := i + 1; j < (len(list) - 1); j++ {
			if list[j].value == 0 {
				continue
			}

			for k := j + 1; k < len(list); k++ {
				if list[k].value == 0 {
					continue
				}

				if list[i].value+list[j].value+list[k].value <= 6 {
					result = append(result, []Cell{list[i], list[j], list[k]})
				}
			}
		}
	}

	return result
}
