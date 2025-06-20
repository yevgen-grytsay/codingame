package main

import (
	"reflect"
	"testing"
)

func TestFindSum(t *testing.T) {
	b := Board{}

	b.ParseAndAddRow("1")
	b.ParseAndAddRow("12")
	b.SetPrizes([]int{100, 100, 100})

	sum := findSum(b)
	want := 300

	if !reflect.DeepEqual(want, sum) {
		t.Errorf(`Actual sum = %v, want match for %v`, sum, want)
	}
}

func TestFindSum_2(t *testing.T) {
	b := Board{}

	b.ParseAndAddRow("1")
	b.ParseAndAddRow("11")
	b.ParseAndAddRow("111")
	b.SetPrizes([]int{100, 200, 100, 100})

	sum := findSum(b)
	want := 600

	if !reflect.DeepEqual(want, sum) {
		t.Errorf(`Actual sum = %v, want match for %v`, sum, want)
	}
}
