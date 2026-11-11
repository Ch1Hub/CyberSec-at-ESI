package main

import (
	"testing"

	"github.com/consensys/gnark-crypto/ecc"
	"github.com/consensys/gnark/test"
)

func TestPreimageCircuit(t *testing.T) {
	assert := test.NewAssert(t)
	var circuit PreimageCircuit

	h42, err := nativeMiMC(42)
	assert.NoError(err)

	// Valid assignment: PreImage = 42, Hash = H42
	assert.SolvingSucceeded(&circuit, &PreimageCircuit{PreImage: 42, Hash: h42}, test.WithCurves(ecc.BN254))

	// Invalid assignment: PreImage = 43, Hash = H42
	assert.SolvingFailed(&circuit, &PreimageCircuit{PreImage: 43, Hash: h42}, test.WithCurves(ecc.BN254))
}
