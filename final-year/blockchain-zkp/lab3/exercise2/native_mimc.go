package main

import (
	"math/big"

	"github.com/consensys/gnark-crypto/ecc/bn254/fr"
	cryptomimc "github.com/consensys/gnark-crypto/ecc/bn254/fr/mimc"
)

func nativeMiMC(x uint64) (*big.Int, error) {
	var value fr.Element
	value.SetUint64(x)
	// One field element: 32 big-endian bytes.
	encoded := value.Bytes()
	hasher := cryptomimc.NewMiMC()
	if _, err := hasher.Write(encoded[:]); err != nil {
		return nil, err
	}
	return new(big.Int).SetBytes(hasher.Sum(nil)), nil
}
