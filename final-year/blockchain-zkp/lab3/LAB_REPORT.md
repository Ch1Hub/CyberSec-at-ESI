# Lab 3: Introduction to Zero-Knowledge Proofs
**Module:** Emergent Security Technologies (ESI-SBA)  
**Academic Year:** 2026–2027  
**Backend & Curve:** Groth16 zk-SNARK over the BN254 scalar field ($\mathbb{F}_r$)

---

## Executive Summary & Project Structure

This repository contains complete implementations, automated tests, and experimental results for Lab 3. The exercises demonstrate the principles of Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge (zk-SNARKs) using [ConsenSys gnark](https://github.com/consensys/gnark).

### Directory Layout

```
.
├── Lab_3 (1).pdf               # Original assignment document
├── go.mod                      # Go module definitions
├── go.sum                      # Go module checksums
├── LAB_REPORT.md               # Complete lab report and question answers
├── exercise1/
│   ├── main.go                 # Exercise 1 implementation & test runner
│   └── circuit_test.go         # Exercise 1 automated test suite
└── exercise2/
    ├── main.go                 # Exercise 2 implementation & test runner
    ├── native_mimc.go          # Out-of-circuit native MiMC reference hasher
    └── circuit_test.go         # Exercise 2 automated test suite
```

### Running the Solutions

1. **Run Exercise 1:**
   ```bash
   go run ./exercise1
   ```
2. **Run Exercise 2:**
   ```bash
   go run ./exercise2
   ```
3. **Run all automated tests:**
   ```bash
   go test -v ./...
   ```

---

## Exercise 1: Generate and Verify a zk-SNARK

### Circuit Statement
Prove knowledge of a private input $x$ satisfying the polynomial relation:
$$x^3 + x + 5 = y$$
where $x$ is secret and $y$ is public.

---

### Questions & Theoretical Analysis

#### Q1.1 Complete the circuit & Explain Public vs. Private
- **Implementation:**
  In gnark's R1CS builder, multiplication is degree-2. We compute intermediate variable $x^2 = \text{Mul}(x, x)$, then $x^3 = \text{Mul}(x^2, x)$, then $\text{Add}(x^3, x, 5)$, and enforce equality to $y$ with `AssertIsEqual`.
- **Why must $y$ be public while $x$ remains private?**
  - **Zero-Knowledge Property:** $x$ represents the secret witness. To preserve privacy, $x$ must never be disclosed to the verifier or included in the public verification input.
  - **Soundness & Instance Identification:** $y$ represents the specific public instance/claim being attested. If $y$ were private, the prover could choose any arbitrary $x$ and any matching $y$, proving only that they know *some* valid pair $(x, y)$, which conveys zero verifiable utility to the verifier. Making $y$ public binds the zero-knowledge proof to the specific statement expected by the verifier.

#### Q1.2 Compile and Set Up
- The circuit compiles into an R1CS (Rank-1 Constraint System) using `frontend.Compile(ecc.BN254.ScalarField(), r1cs.NewBuilder, &circuit)`.
- It produces **3 R1CS constraints**:
  1. $x \cdot x = x^2$
  2. $x^2 \cdot x = x^3$
  3. $1 \cdot (x^3 + x + 5) = y$
- `groth16.Setup(ccs)` performs the preprocessing step (trusted setup) to produce the Proving Key (`pk`) and Verification Key (`vk`).

#### Q1.3 Generate a Proof
- Assignment: $x = 3, y = 35$ ($3^3 + 3 + 5 = 27 + 3 + 5 = 35$).
- Prover compiles the full witness using `frontend.NewWitness(&assignment, ecc.BN254.ScalarField())` and executes `groth16.Prove(ccs, pk, witness)`.
- The full witness contains both secret ($x=3$) and public ($y=35$) assignments and remains strictly on the prover side.

#### Q1.4 Verify the Proof & Witness Separation
- The verifier is provided with the verification key `vk`, the proof $\pi$, and the public witness containing only $y = 35$ (extracted using `witness.Public()`).
- `groth16.Verify(proof, vk, publicWitness)` evaluates the pairing equation $e(A, B) = e(\alpha, \beta) + e(x_{\text{pub}}, \gamma) + e(C, \delta)$ and returns `nil` (Success).
- **Why is the full witness not sent to the verifier?**
  Sending the full witness would transmit $x = 3$ to the verifier, destroying the zero-knowledge guarantee. The zk-SNARK allows the verifier to become mathematically convinced that a valid $x$ exists without learning anything about $x$.

#### Q1.5 Try an Invalid Witness ($x = 4, y = 35$)
- **Evaluation:** For $x = 4$: $4^3 + 4 + 5 = 64 + 4 + 5 = 73 \neq 35$.
- **Observed Stage:** Proof generation stage (`groth16.Prove`), specifically during the R1CS constraint system solver step before cryptographic exponentiations.
- **Error Recorded:**
  ```text
  constraint #2 is not satisfied: 1 ⋅ 73 != 35
  ```
- **Conclusion:** The pair does not satisfy the arithmetic constraints of the circuit; the prover refuses to generate a proof for a false statement.

#### Q1.6 Change the Public Input ($y = 36$ with original proof)
- The valid proof generated for $y = 35$ is checked against public witness $y = 36$ without modifying the proof or keys.
- **Verification Result:** FAILED with error:
  ```text
  pairing doesn't match
  ```
- **Interpretation:** In Groth16, the public inputs enter linearly into the verification pairing equation:
  $$e\left(\sum_{i=0}^{l} w_i K_i, [\gamma]_2\right)$$
  The proof is cryptographically tied to the exact public inputs used during its generation. An attacker cannot replay or repurpose a valid proof for a different public value.

#### Q1.7 Interpret the Components
- **Private Witness ($w_{\text{secret}}$):** `Circuit.X = 3` (known only to the prover).
- **Public Input ($w_{\text{pub}}$):** `Circuit.Y = 35` (known to prover and verifier).
- **Proof ($\pi$):** Group elements in BN254: $\pi = (A \in G_1, B \in G_2, C \in G_1)$.
- **Proving Key (`pk`):** Contains encrypted evaluation points of Lagrange/QAP polynomials enabling the prover to compute $A, B, C$.
- **Verification Key (`vk`):** Contains $[\alpha]_1, [\beta]_2, [\gamma]_2, [\delta]_2$ and $[K_i(\tau)]_1$ for public inputs, allowing fast verification via elliptic curve pairings.

---

### Exercise 1 Observations Table

| Test | Result / Error Observed |
|---|---|
| **Generate and verify with $x = 3, y = 35$** | **SUCCESS** (`nil` error; Verification result: SUCCESS) |
| **Try to prove with $x = 4, y = 35$** | **FAILED** during `groth16.Prove` solver: `constraint #2 is not satisfied: 1 ⋅ 73 != 35` |
| **Verify the original proof with $y = 36$** | **FAILED** during `groth16.Verify`: `pairing doesn't match` |

---

## Exercise 2: Prove Knowledge of a Hash Preimage

### Circuit Statement
Prove knowledge of private preimage $x$ such that:
$$\text{MiMC}(x) = H$$
where $x$ is secret, $H$ is public digest, and MiMC is an algebraic SNARK-friendly hash function over $\mathbb{F}_r$ (BN254).

---

### Questions & Theoretical Analysis

#### Q2.1 Complete the Circuit
- Implemented using gnark's `github.com/consensys/gnark/std/hash/mimc`.
- `mimc.NewMiMC(api)` initializes the in-circuit hasher with BN254 round constants.
- The circuit writes `c.PreImage`, computes the digest with `hasher.Sum()`, and enforces `api.AssertIsEqual(computedHash, c.Hash)`.

#### Q2.2 Prepare Public Digest & Compare $H_{42}$ vs $H_{43}$
- Native MiMC execution:
  - $H_{42} = \text{nativeMiMC}(42) =$ `0x15cc289ebc18cb3ba9301f46f0619391ee79007ea289fd3d9155d574f121e953`  
    *(Decimal: $9859286970797740035380527431348382675909558438535884267813507963157263542611$)*
  - $H_{43} = \text{nativeMiMC}(43) =$ `0x23702a91c9aeaff00942157ba9001119a5f3f22a65135bc27d46d684574ee9bc`  
    *(Decimal: $16029130375447967373014155158173112316002222959924145978006334861362666072508$)*
  - Confirmed $H_{42} \neq H_{43}$ (preimage sensitivity / collision resistance).
- **Why must a native hash computation and the circuit use the same encoding and hash function?**
  Arithmetic circuits operate directly over prime fields ($\mathbb{F}_r$). MiMC applies non-linear round transformations ($x \mapsto (x + k + c_i)^7$ or $5$) over field elements. If the native hashing outside the circuit uses different endianness, modulus, padding, or permutation constants than the in-circuit gadget, the native digest $H$ will not equal the in-circuit evaluated digest, causing the constraint `AssertIsEqual` to fail even if the prover intended the same numerical input.

#### Q2.3 Compile and Set Up
- Compiled using `frontend.Compile(ecc.BN254.ScalarField(), r1cs.NewBuilder, &circuit)`.
- Number of constraints generated: **331 constraints** (corresponding to 110 rounds of MiMC-7 with S-box additions/multiplications plus final equality check).
- Proving and verification keys generated with `groth16.Setup(ccs)`.

#### Q2.4 Prove and Verify ($x = 42, H = H_{42}$)
- Prover sets `PreImage = 42, Hash = H42`.
- Proof generated cleanly; verifier verifies with public witness containing only $H_{42}$.
- Result: **SUCCESS** (`nil` error).

#### Q2.5 Try Incorrect Preimage ($x = 43, H = H_{42}$)
- Prover attempts to generate a proof with $x = 43$ and claimed hash $H_{42}$.
- **Stage of failure:** Proof generation stage (`groth16.Prove`).
- **Error Recorded:**
  ```text
  constraint #330 is not satisfied: 1 ⋅ 16029130375447967373014155158173112316002222959924145978006334861362666072508 != 9859286970797740035380527431348382675909558438535884267813507963157263542611
  ```
- **Analysis:** Constraint #330 is the final `AssertIsEqual` constraint between the computed digest ($\text{MiMC}(43)$) and the declared public digest ($H_{42}$). Since they are unequal, constraint satisfaction fails and no valid proof can be synthesized.

---

### Exercise 2 Observations Table

| Test | Result / Error Observed |
|---|---|
| **Generate and verify with $x = 42, H = H_{42}$** | **SUCCESS** (`nil` error; Verification result: SUCCESS) |
| **Try to prove with $x = 43, H = H_{42}$** | **FAILED** during `groth16.Prove` solver at constraint #330: `1 ⋅ 16029130375447967373014155158173112316002222959924145978006334861362666072508 != 9859286970797740035380527431348382675909558438535884267813507963157263542611` |

---

## Conclusion

This lab successfully showcases the core lifecycle of zero-knowledge proofs with Groth16:
1. **Arithmetic circuit formulation** ($x^3 + x + 5 = y$ and MiMC hash).
2. **Setup ceremony** yielding PK and VK.
3. **Soundness & Completeness:** Valid witnesses produce verifiable proofs; invalid witnesses fail constraint satisfaction during proof generation.
4. **Input Binding:** Public inputs are cryptographically committed to the proof; modifying public inputs invalidates the verification pairing.
