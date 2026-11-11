package main

import (
	"fmt"

	"github.com/consensys/gnark-crypto/ecc"
	"github.com/consensys/gnark/backend/groth16"
	"github.com/consensys/gnark/frontend"
	"github.com/consensys/gnark/frontend/cs/r1cs"
)

// Circuit defines the arithmetic circuit: X^3 + X + 5 == Y
type Circuit struct {
	X frontend.Variable // Private input
	Y frontend.Variable `gnark:",public"` // Public input
}

// Define declares the circuit's constraints
func (c *Circuit) Define(api frontend.API) error {
	// x^2 = x * x
	x2 := api.Mul(c.X, c.X)
	// x^3 = x^2 * x
	x3 := api.Mul(x2, c.X)
	// x^3 + x + 5
	res := api.Add(x3, c.X, 5)
	// Constrain res == Y
	api.AssertIsEqual(res, c.Y)
	return nil
}

func main() {
	fmt.Println("=== Lab 3 - Exercise 1: Generate and Verify a zk-SNARK ===")

	// Q1.2: Compile the circuit into an R1CS
	var circuit Circuit
	ccs, err := frontend.Compile(ecc.BN254.ScalarField(), r1cs.NewBuilder, &circuit)
	if err != nil {
		panic(fmt.Sprintf("frontend.Compile failed: %v", err))
	}
	fmt.Printf("Circuit compiled successfully. Number of constraints: %d\n", ccs.GetNbConstraints())

	// Set up Groth16 proving and verification keys
	pk, vk, err := groth16.Setup(ccs)
	if err != nil {
		panic(fmt.Sprintf("groth16.Setup failed: %v", err))
	}
	fmt.Println("Groth16 setup completed successfully (PK and VK generated).")

	// Q1.3: Generate a proof with valid witness x = 3, y = 35
	fmt.Println("\n--- Test 1: Valid assignment (x = 3, y = 35) ---")
	assignmentValid := Circuit{
		X: 3,
		Y: 35,
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

	// Q1.4: Verify the proof with public witness (y = 35)
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

	// Q1.5: Try an invalid witness (x = 4, y = 35)
	fmt.Println("\n--- Test 2: Invalid witness (x = 4, y = 35) ---")
	assignmentInvalid := Circuit{
		X: 4,
		Y: 35,
	}
	witnessInvalid, err := frontend.NewWitness(&assignmentInvalid, ecc.BN254.ScalarField())
	if err != nil {
		fmt.Printf("Error building witness for invalid assignment: %v\n", err)
	} else {
		_, errProof := groth16.Prove(ccs, pk, witnessInvalid)
		if errProof != nil {
			fmt.Printf("groth16.Prove failed as expected at proof generation stage: %v\n", errProof)
		} else {
			fmt.Println("Warning: Proof generation succeeded unexpectedly for invalid witness.")
		}
	}

	// Q1.6: Change public input: verify original valid proof with y = 36
	fmt.Println("\n--- Test 3: Modified public input (original proof from Q1.3 with y = 36) ---")
	assignmentTamperedPublic := Circuit{
		Y: 36,
	}
	publicWitnessTampered, err := frontend.NewWitness(&assignmentTamperedPublic, ecc.BN254.ScalarField(), frontend.PublicOnly())
	if err != nil {
		panic(fmt.Sprintf("frontend.NewWitness for public input failed: %v", err))
	}

	errVerifyTampered := groth16.Verify(proofValid, vk, publicWitnessTampered)
	if errVerifyTampered != nil {
		fmt.Printf("Verification with y = 36 failed as expected: %v\n", errVerifyTampered)
	} else {
		fmt.Println("Warning: Verification succeeded unexpectedly with tampered public input.")
	}
}
