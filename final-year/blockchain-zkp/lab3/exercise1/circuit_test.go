package main

import (
	"testing"

	"github.com/consensys/gnark-crypto/ecc"
	"github.com/consensys/gnark/test"
)

func TestCircuit(t *testing.T) {
	assert := test.NewAssert(t)
	var circuit Circuit

	// Valid assignment: x = 3, y = 35 -> 3^3 + 3 + 5 = 27 + 3 + 5 = 35
	assert.SolvingSucceeded(&circuit, &Circuit{X: 3, Y: 35}, test.WithCurves(ecc.BN254))

	// Invalid assignment: x = 4, y = 35 -> 4^3 + 4 + 5 = 73 != 35
	assert.SolvingFailed(&circuit, &Circuit{X: 4, Y: 35}, test.WithCurves(ecc.BN254))
}
