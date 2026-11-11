package main

import (
	"fmt"

	"github.com/consensys/gnark-crypto/ecc"
	"github.com/consensys/gnark/backend/groth16"
	"github.com/consensys/gnark/frontend"
	"github.com/consensys/gnark/frontend/cs/r1cs"
	"github.com/consensys/gnark/std/hash/mimc"
)

// PreimageCircuit proves knowledge of preimage x such that MiMC(x) == Hash
type PreimageCircuit struct {
	PreImage frontend.Variable // Private input
	Hash     frontend.Variable `gnark:",public"` // Public digest
}

// Define declares the circuit's constraints
func (c *PreimageCircuit) Define(api frontend.API) error {
	// Q2.1: Create in-circuit MiMC hasher and check error
	hasher, err := mimc.NewMiMC(api)
	if err != nil {
		return err
	}

	// Hash the private preimage
	hasher.Write(c.PreImage)
	computedHash := hasher.Sum()

	// Constrain computedHash to equal the public Hash
	api.AssertIsEqual(computedHash, c.Hash)
	return nil
}

func main() {
	fmt.Println("=== Lab 3 - Exercise 2: Prove Knowledge of a Hash Preimage ===")

	// Q2.2: Prepare public digests outside circuit using nativeMiMC
	h42, err := nativeMiMC(42)
	if err != nil {
		panic(fmt.Sprintf("nativeMiMC(42) failed: %v", err))
	}
	fmt.Printf("Native MiMC(42) digest H42: 0x%s\n", h42.Text(16))

	h43, err := nativeMiMC(43)
	if err != nil {
		panic(fmt.Sprintf("nativeMiMC(43) failed: %v", err))
	}
	fmt.Printf("Native MiMC(43) digest H43: 0x%s\n", h43.Text(16))

	if h42.Cmp(h43) == 0 {
		panic("Collision detected or hashes unexpectedly match!")
	}
	fmt.Println("Confirmed H42 != H43 (digests differ as expected).")

	// Q2.3: Compile PreimageCircuit and set up Groth16 keys
	var circuit PreimageCircuit
	ccs, err := frontend.Compile(ecc.BN254.ScalarField(), r1cs.NewBuilder, &circuit)
	if err != nil {
		panic(fmt.Sprintf("frontend.Compile failed: %v", err))
	}
	fmt.Printf("Circuit compiled successfully. Number of constraints: %d\n", ccs.GetNbConstraints())

	pk, vk, err := groth16.Setup(ccs)
	if err != nil {
		panic(fmt.Sprintf("groth16.Setup failed: %v", err))
	}
	fmt.Println("Groth16 setup completed successfully (PK and VK generated).")

	// Q2.4: Prove and verify with valid preimage x = 42, Hash = H42
	fmt.Println("\n--- Test 1: Valid preimage (x = 42, Hash = H42) ---")
	assignmentValid := PreimageCircuit{
		PreImage: 42,
		Hash:     h42,
	}
	witnessValid, err := frontend.NewWitness(&assignmentValid, ecc.BN254.ScalarField())
	if err != nil {
		panic(fmt.Sprintf("frontend.NewWitness failed: %v", err))
	}

	proofValid, err := groth16.Prove(ccs, pk, witnessValid)
	if err != nil {
		panic(fmt.Sprintf("groth16.Prove failed: %v", err))
	}
	fmt.Println("Proof generated successfully.")

	publicWitnessValid, err := witnessValid.Public()
	if err != nil {
		panic(fmt.Sprintf("witnessValid.Public failed: %v", err))
	}

	err = groth16.Verify(proofValid, vk, publicWitnessValid)
	if err != nil {
		fmt.Printf("Verification result: FAILED (%v)\n", err)
	} else {
		fmt.Println("Verification result: SUCCESS (nil error)")
	}

	// Q2.5: Try an incorrect preimage (x = 43, Hash = H42)
	fmt.Println("\n--- Test 2: Invalid preimage (x = 43, Hash = H42) ---")
	assignmentInvalid := PreimageCircuit{
		PreImage: 43,
		Hash:     h42,
	}
	witnessInvalid, err := frontend.NewWitness(&assignmentInvalid, ecc.BN254.ScalarField())
	if err != nil {
		fmt.Printf("Error building witness: %v\n", err)
	} else {
		_, errProof := groth16.Prove(ccs, pk, witnessInvalid)
		if errProof != nil {
			fmt.Printf("groth16.Prove failed as expected at proof generation stage: %v\n", errProof)
		} else {
			fmt.Println("Warning: Proof generation succeeded unexpectedly for invalid preimage.")
		}
	}
}
