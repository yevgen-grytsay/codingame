package main

import (
	"reflect"
	"testing"
)

func TestGetRootNode(t *testing.T) {
	b := Board{}

	b.ParseAndAddRow("3")
	b.ParseAndAddRow("12")
	b.ParseAndAddRow("121")
	b.SetPrizes([]int{100, 200, 200, 100})

	rootNode := b.GetRootNode()

	wantRootNode := Node{row: 0, col: 0, value: 3}
	if !reflect.DeepEqual(wantRootNode, rootNode) {
		t.Errorf(`Actual root node = %v, want match for %v`, rootNode, wantRootNode)
	}
}

func TestGetNeighbors_1(t *testing.T) {
	b := Board{}

	b.ParseAndAddRow("3")
	b.ParseAndAddRow("12")
	b.ParseAndAddRow("121")
	b.SetPrizes([]int{100, 200, 200, 100})

	rootNode := b.GetRootNode()

	nodeA, nodeB := b.GetNeighbors(rootNode)
	wantNodeA := Node{row: 1, col: 0, value: 1}
	wantNodeB := Node{row: 1, col: 1, value: 2}

	if !reflect.DeepEqual(wantNodeA, nodeA) {
		t.Errorf(`Actual left node = %v, want match for %v`, nodeA, wantNodeA)
	}

	if !reflect.DeepEqual(wantNodeB, nodeB) {
		t.Errorf(`Actual right node = %v, want match for %v`, nodeB, wantNodeB)
	}
}

func TestGetNeighbors_2(t *testing.T) {
	b := Board{}

	b.ParseAndAddRow("3")
	b.ParseAndAddRow("12")
	b.ParseAndAddRow("121")
	b.SetPrizes([]int{100, 200, 200, 100})

	node := Node{row: 1, col: 1, value: 2}

	nodeA, nodeB := b.GetNeighbors(node)
	wantNodeA := Node{row: 2, col: 1, value: 2}
	wantNodeB := Node{row: 2, col: 2, value: 1}

	if !reflect.DeepEqual(wantNodeA, nodeA) {
		t.Errorf(`Actual left node = %v, want match for %v`, nodeA, wantNodeA)
	}

	if !reflect.DeepEqual(wantNodeB, nodeB) {
		t.Errorf(`Actual right node = %v, want match for %v`, nodeB, wantNodeB)
	}
}

func TestGetNeighborsError(t *testing.T) {
	b := Board{}

	b.ParseAndAddRow("3")
	b.ParseAndAddRow("12")
	b.SetPrizes([]int{100, 200, 200, 100})

	node := Node{row: 1, col: 0, value: 1}

	expectedMessage := "invalid row index 2 (total rows: 2)"
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected a panic, but none occurred.")
		} else if r != expectedMessage {
			t.Errorf("Expected panic with message 'invalid row index 2 (total rows: 2)', but got: %v", r)
		}
	}()

	b.GetNeighbors(node)
}
