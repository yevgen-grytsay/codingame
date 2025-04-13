package main

import (
	"reflect"
	"strconv"
	"strings"
	"testing"
)

func createState(width int, height int, rows []string) Board {
	state := Board{
		width:  width,
		height: height,
		grid:   make([][]Cell, height),
	}
	for i := range height {
		values := strings.Split(rows[i], "")
		state.grid[i] = make([]Cell, width)

		for j := range width {
			intVal, _ := strconv.Atoi(values[j])
			state.grid[i][j] = Cell{row: i, col: j, index: i*width + j, value: intVal}
		}
	}

	return state
}

func TestCreateState(t *testing.T) {
	state := createState(3, 3, []string{
		"010",
		"222",
		"101",
	})

	want := Board{
		width:  3,
		height: 3,
		grid: [][]Cell{
			{
				{row: 0, col: 0, index: 0, value: 0},
				{row: 0, col: 1, index: 1, value: 1},
				{row: 0, col: 2, index: 2, value: 0},
			},
			{
				{row: 1, col: 0, index: 3, value: 2},
				{row: 1, col: 1, index: 4, value: 2},
				{row: 1, col: 2, index: 5, value: 2},
			},
			{
				{row: 2, col: 0, index: 6, value: 1},
				{row: 2, col: 1, index: 7, value: 0},
				{row: 2, col: 2, index: 8, value: 1},
			},
		},
	}

	if !reflect.DeepEqual(want, state) {
		t.Errorf(`Actual state = %#v, want match for %#v`, state, want)
	}
}

func TestGetAdjacent(t *testing.T) {
	state := createState(3, 3, []string{
		"010",
		"222",
		"101",
	})

	want := []Cell{
		{row: 0, col: 1, index: 1, value: 1},
		{row: 1, col: 0, index: 3, value: 2},
		{row: 1, col: 2, index: 5, value: 2},
		{row: 2, col: 1, index: 7, value: 0},
	}

	adjacent := state.getAdjacent(1, 1)

	if !reflect.DeepEqual(want, adjacent) {
		t.Errorf(`Actual state = %#v, want match for %#v`, adjacent, want)
	}
}

func TestGetAdjacent2(t *testing.T) {
	state := createState(3, 3, []string{
		"010",
		"222",
		"101",
	})

	want := []Cell{
		{row: 0, col: 1, index: 1, value: 1},
		{row: 1, col: 0, index: 3, value: 2},
	}

	adjacent := state.getAdjacent(0, 0)

	if !reflect.DeepEqual(want, adjacent) {
		t.Errorf(`Actual state = %#v, want match for %#v`, adjacent, want)
	}
}

func TestSearch(t *testing.T) {
	state := createState(3, 3, []string{
		"010",
		"022",
		"000",
	})

	want := []Cell{
		{row: 0, col: 1, index: 1, value: 1},
	}

	next := state.search(1, 1)

	if !reflect.DeepEqual(want, next) {
		t.Errorf(`Actual state = %#v, want match for %#v`, next, want)
	}
}

func TestSearch2(t *testing.T) {
	state := createState(3, 3, []string{
		"010",
		"022",
		"010",
	})

	want := []Cell{
		{row: 0, col: 1, index: 1, value: 1},
		{row: 2, col: 1, index: 7, value: 1},
	}

	next := state.search(1, 1)

	if !reflect.DeepEqual(want, next) {
		t.Errorf(`Actual state = %#v, want match for %#v`, next, want)
	}
}
