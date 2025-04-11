package main

import (
	"reflect"
	"strconv"
	"strings"
	"testing"
)

// TestHelloName calls greetings.Hello with a name, checking
// for a valid return value.
func TestSample2Simple(t *testing.T) {
	want := [][]Cell{
		{{index: 0, value: 1}, {index: 2, value: 1}},
	}

	list := []Cell{
		{index: 0, value: 1},
		{index: 2, value: 1},
	}

	actual := sample2(list)

	if !reflect.DeepEqual(want, actual) {
		t.Errorf(`Sample2 = %v, want match for %#q`, actual, want)
	}
}

func TestSample2(t *testing.T) {
	tests := []struct {
		list []Cell
		want [][]Cell
	}{
		{
			list: []Cell{
				{index: 0, value: 1},
				{index: 2, value: 1},
			},
			want: [][]Cell{
				{
					{index: 0, value: 1},
					{index: 2, value: 1},
				},
			},
		},
		{
			list: []Cell{
				{index: 0, value: 1},
				{index: 2, value: 3},
				{index: 4, value: 5},
			},
			want: [][]Cell{
				{
					{index: 0, value: 1},
					{index: 2, value: 3},
				},
				{
					{index: 0, value: 1},
					{index: 4, value: 5},
				},
				// { sum is greater than 6
				// 	{index: 2, value: 3},
				// 	{index: 4, value: 5},
				// },
			},
		},
		{
			list: []Cell{
				{index: 0, value: 1},
				{index: 2, value: 3},
				{index: 4, value: 3},
			},
			want: [][]Cell{
				{
					{index: 0, value: 1},
					{index: 2, value: 3},
				},
				{
					{index: 0, value: 1},
					{index: 4, value: 3},
				},
				{
					{index: 2, value: 3},
					{index: 4, value: 3},
				},
			},
		},
	}

	for i, testData := range tests {
		actual := sample2(testData.list)

		if !reflect.DeepEqual(testData.want, actual) {
			t.Errorf(`[%d] Sample2 = %v, want match for %#q`, i, actual, testData.want)
		}
	}
}

func TestSample3(t *testing.T) {
	tests := []struct {
		list []Cell
		want [][]Cell
	}{
		{
			list: []Cell{
				{index: 0, value: 1},
				{index: 2, value: 1},
				{index: 4, value: 1},
			},
			want: [][]Cell{
				{
					{index: 0, value: 1},
					{index: 2, value: 1},
					{index: 4, value: 1},
				},
			},
		},
		{
			list: []Cell{
				{index: 0, value: 1},
				{index: 2, value: 1},
				{index: 4, value: 5},
			},
			want: [][]Cell{},
		},
		{
			list: []Cell{
				{index: 1, value: 1},
				{index: 3, value: 1},
				{index: 5, value: 1},
				{index: 7, value: 1},
			},
			want: [][]Cell{
				{
					{index: 1, value: 1},
					{index: 3, value: 1},
					{index: 5, value: 1},
				},
				{
					{index: 1, value: 1},
					{index: 3, value: 1},
					{index: 7, value: 1},
				},
				{
					{index: 1, value: 1},
					{index: 5, value: 1},
					{index: 7, value: 1},
				},
				{
					{index: 3, value: 1},
					{index: 5, value: 1},
					{index: 7, value: 1},
				},
			},
		},
	}

	for i, testData := range tests {
		actual := sample3(testData.list)

		if len(actual) == 0 && len(testData.want) == 0 {
			continue
		}

		if !reflect.DeepEqual(testData.want, actual) {
			t.Errorf(`[%d] Sample3 = %v, want match for %v`, i, actual, testData.want)
		}
	}
}

func TestGetNeighbors3(t *testing.T) {
	state := State{
		grid: []Cell{
			{index: 0, value: 1},
			{index: 1, value: 1},
			{index: 2, value: 1},
			{index: 3, value: 1},
			{index: 4, value: 1},
			{index: 5, value: 1},
			{index: 6, value: 1},
			{index: 7, value: 1},
			{index: 8, value: 1},
		},
	}

	actual := state.getNeighbors(Cell{index: 1})

	want := []Cell{
		{index: 0, value: 1},
		{index: 2, value: 1},
		{index: 4, value: 1},
	}

	if !reflect.DeepEqual(want, actual) {
		t.Errorf(`Actual neighbors = %v, want match for %v`, actual, want)
	}
}

func TestGetNeighbors4(t *testing.T) {
	state := State{
		grid: []Cell{
			{index: 0, value: 1},
			{index: 1, value: 1},
			{index: 2, value: 1},
			{index: 3, value: 1},
			{index: 4, value: 1},
			{index: 5, value: 1},
			{index: 6, value: 1},
			{index: 7, value: 1},
			{index: 8, value: 1},
		},
	}

	actual := state.getNeighbors(Cell{index: 4})

	want := []Cell{
		{index: 1, value: 1},
		{index: 3, value: 1},
		{index: 5, value: 1},
		{index: 7, value: 1},
	}

	if !reflect.DeepEqual(want, actual) {
		t.Errorf(`Actual neighbors = %v, want match for %v`, actual, want)
	}
}

func TestGetNeighbors2(t *testing.T) {
	state := State{
		grid: []Cell{
			{index: 0, value: 1},
			{index: 1, value: 1},
			{index: 2, value: 1},
			{index: 3, value: 1},
			{index: 4, value: 1},
			{index: 5, value: 1},
			{index: 6, value: 1},
			{index: 7, value: 1},
			{index: 8, value: 1},
		},
	}

	actual := state.getNeighbors(Cell{index: 8})

	want := []Cell{
		{index: 5, value: 1},
		{index: 7, value: 1},
	}

	if !reflect.DeepEqual(want, actual) {
		t.Errorf(`Actual neighbors = %v, want match for %v`, actual, want)
	}
}

func TestWithout(t *testing.T) {
	state := createState([]string{
		"111",
		"111",
		"111",
	})

	newState := state.without(5)

	wantState := createState([]string{
		"111",
		"111",
		"111",
	})

	wantNewState := createState([]string{
		"111",
		"110",
		"111",
	})

	if !reflect.DeepEqual(wantState, state) {
		t.Errorf(`Actual state = %v, want match for %v`, state, wantState)
	}

	if !reflect.DeepEqual(wantNewState, newState) {
		t.Errorf(`Actual state = %v, want match for %v`, newState, wantNewState)
	}
}

func TestGetFree(t *testing.T) {
	state := State{
		grid: []Cell{
			{index: 0, value: 1},
			{index: 1, value: 1},
			{index: 2, value: 1},
			{index: 3, value: 0},
			{index: 4, value: 1},
			{index: 5, value: 1},
			{index: 6, value: 1},
			{index: 7, value: 0},
			{index: 8, value: 1},
		},
	}

	actual := state.getFree()

	want := []Cell{
		{index: 3, value: 0},
		{index: 7, value: 0},
	}

	if !reflect.DeepEqual(want, actual) {
		t.Errorf(`Actual state = %v, want match for %v`, actual, want)
	}
}

func TestHash(t *testing.T) {
	state := State{
		grid: []Cell{
			{index: 0, value: 0},
			{index: 1, value: 1},
			{index: 2, value: 2},
			{index: 3, value: 3},
			{index: 4, value: 4},
			{index: 5, value: 5},
			{index: 6, value: 6},
			{index: 7, value: 7},
			{index: 8, value: 8},
		},
	}

	actual := state.hash()
	want := 12345678

	if actual != want {
		t.Errorf(`Actual hash = %v, want match for %v`, actual, want)
	}
}

func TestPutState1(t *testing.T) {
	state := createState([]string{
		"000",
		"000",
		"000",
	})

	actual := put(state, 4)

	want := []State{
		createState([]string{
			"000",
			"010",
			"000",
		}),
	}

	if !reflect.DeepEqual(want, actual) {
		t.Errorf(`Actual states = %v, want match for %v`, actual, want)
	}
}

func TestPutState2(t *testing.T) {
	state := createState([]string{
		"010",
		"200",
		"000",
	})

	actual := put(state, 0)

	want := []State{
		createState([]string{
			"300",
			"000",
			"000",
		}),
	}

	if !reflect.DeepEqual(want, actual) {
		t.Errorf(`Actual states = %v, want match for %v`, actual, want)
	}
}

func TestPutState3(t *testing.T) {
	state := createState([]string{
		"040",
		"300",
		"000",
	})

	actual := put(state, 0)

	want := []State{
		createState([]string{
			"140",
			"300",
			"000",
		}),
	}

	if !reflect.DeepEqual(want, actual) {
		t.Errorf(`Actual states = %v, want match for %v`, actual, want)
	}
}
func TestPutStateThreeStates(t *testing.T) {
	state := createState([]string{
		"202",
		"030",
		"000",
	})

	actual := put(state, 1)

	want := []State{
		createState([]string{
			"052",
			"000",
			"000",
		}),
		createState([]string{
			"250",
			"000",
			"000",
		}),
		createState([]string{
			"040",
			"030",
			"000",
		}),
	}

	if !reflect.DeepEqual(want, actual) {
		t.Errorf(`Actual states = %v, want match for %v`, actual, want)
	}
}

func TestCrawler(t *testing.T) {
	state := createState([]string{
		"666",
		"606",
		"666",
	})

	crawler := NewCrawler(10)
	actual := crawler.run(state)

	want := 666616666

	if want != actual {
		t.Errorf(`Actual states = %v, want match for %v`, actual, want)
	}
}

func createState(rows []string) State {

	var i int
	state := State{grid: make([]Cell, 9)}
	for _, row := range rows {
		values := strings.Split(row, "")
		for _, strValue := range values {
			intVal, _ := strconv.Atoi(strValue)
			state.grid[i] = Cell{index: i, value: intVal}
			i++
		}
	}

	return state
}

func TestGame1(t *testing.T) {
	state := createState([]string{
		"060",
		"222",
		"161",
	})

	crawler := NewCrawler(20)
	sum := crawler.handle(state, crawler.depth)

	if sum == 0 {
		t.Errorf(`Sum = %v`, sum)
	}
}

func TestGame2(t *testing.T) {
	state := createState([]string{
		"555",
		"005",
		"555",
	})

	crawler := NewCrawler(1)
	sum := crawler.handle(state, crawler.depth)

	if sum == 0 {
		t.Errorf(`Sum = %v`, sum)
	}
}

func TestCodinGame1(t *testing.T) {
	state := createState([]string{
		"060",
		"222",
		"161",
	})

	crawler := NewCrawler(20)
	sum := crawler.run(state)

	want := 322444322

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}

func TestCodinGame2(t *testing.T) {
	state := createState([]string{
		"506",
		"450",
		"064",
	})

	crawler := NewCrawler(20)
	sum := crawler.run(state)

	want := 951223336

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}

func TestCodinGame3(t *testing.T) {
	state := createState([]string{
		"555",
		"005",
		"555",
	})

	crawler := NewCrawler(1)
	sum := crawler.run(state)

	want := 36379286

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}

func TestCodinGame4(t *testing.T) {
	state := createState([]string{
		"616",
		"101",
		"616",
	})

	crawler := NewCrawler(1)
	sum := crawler.run(state)

	want := 264239762

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}

func TestCodinGame5(t *testing.T) {
	state := createState([]string{
		"606",
		"000",
		"615",
	})

	crawler := NewCrawler(8)
	sum := crawler.run(state)

	want := 76092874

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}

func TestCodinGame6(t *testing.T) {
	state := createState([]string{
		"300",
		"362",
		"102",
	})

	crawler := NewCrawler(24)
	sum := crawler.run(state)

	want := 661168294

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}

func TestCodinGame7(t *testing.T) {
	state := createState([]string{
		"604",
		"202",
		"400",
	})

	crawler := NewCrawler(36)
	sum := crawler.run(state)

	want := 350917228

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}

func TestCodinGame8(t *testing.T) {
	state := createState([]string{
		"000",
		"054",
		"105",
	})

	crawler := NewCrawler(32)
	sum := crawler.run(state)

	want := 999653138

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}

func TestCodinGame9(t *testing.T) {
	state := createState([]string{
		"004",
		"024",
		"134",
	})

	crawler := NewCrawler(40)
	sum := crawler.run(state)

	want := 521112022

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}

func TestCodinGame10(t *testing.T) {
	state := createState([]string{
		"054",
		"030",
		"030",
	})

	crawler := NewCrawler(40)
	sum := crawler.run(state)

	want := 667094338

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}

func TestCodinGame11(t *testing.T) {
	// t.Skip("Not fixed yet")
	state := createState([]string{
		"051",
		"000",
		"401",
	})

	crawler := NewCrawler(20)
	sum := crawler.run(state)

	want := 738691369

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}

func TestCodinGame12(t *testing.T) {
	state := createState([]string{
		"100",
		"352",
		"100",
	})

	crawler := NewCrawler(20)
	sum := crawler.run(state)

	want := 808014757

	if sum != want {
		t.Errorf(`Sum = %d, want match for %d`, sum, want)
	}
}
