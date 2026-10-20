# Lab 2 Report: Blockchain Platforms and Smart Contracts
**Module:** Emergent Security Technologies — ESI-SBA  
**Academic Year:** 2026-2027  
**Platform:** Ethereum / EVM (Ganache, Solidity `^0.8.20`, Remix IDE / JSON-RPC)

---

## Part 1: Install and Run Ganache

### Q1.1 Installed Versions & Ganache Verification
- **Node.js Version:** `v22.17.0` (checked via `node --version`)
- **npm Version:** `10.9.2` (checked via `npm --version`)
- **Ganache Installation Command:**
  ```bash
  npm install --global ganache
  ```
- **Verification Command:**
  ```bash
  ganache --version
  ```
  *Output:* `ganache v7.9.2 (@ganache/cli: 0.10.2, @ganache/core: 0.10.2)`

---

### Q1.2 RPC Server Address
Starting Ganache reveals the RPC listening endpoint:
```text
RPC Listening on 127.0.0.1:8545
```
- **RPC Server Address:** `http://127.0.0.1:8545` (Network ID / Chain ID: `1337`)

---

### Q1.3 Test Accounts and Initial Balances
- **Number of Test Accounts Created:** Exactly **10 accounts** (indexed `(0)` to `(9)`).
- **Initial Balance per Account:** **1000 ETH** (`1000000000000000000000 wei`) each.

---

### Q1.4 Account Public Address and Private Key Purpose
Taking Account `(0)` as an example from the Ganache output:
- **Public Address:** `0x15aC6d7F4e5C685baBF0b0023Ed0240d7e5b244C`
  - **Purpose:** Acts as the public identity and destination address on the blockchain (derived from the public key via Keccak-256). It is safely shareable and used by other entities to send funds or identify contract interactions.
- **Private Key:** `0x<REDACTED_GANACHE_TEST_PRIVATE_KEY>`
  - **Purpose:** Secret 256-bit cryptographic scalar used to sign transactions and prove ownership of the account's assets. Anyone possessing the private key possesses full control over the funds.

---

### Q1.5 Role of the JSON-RPC Interface
The **JSON-RPC interface** is the standardized remote procedure call specification (encoded in JSON) that allows external clients—such as web browsers, Web3 libraries (`ethers.js`, `web3.js`), or developer IDEs like **Remix**—to communicate with the Ethereum client (Ganache).  
Through standard JSON-RPC methods (`eth_accounts`, `eth_sendTransaction`, `eth_call`, `eth_getBlockByNumber`), Remix can query accounts, deploy compiled bytecode, broadcast transactions, and read contract state from Ganache.

---

## Part 2: Write and Deploy a Smart Contract with Remix

### Q2.1 to Q2.3 Complete `SimpleStorage.sol`
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleStorage {
    // Q2.1: Public state variable named valeur
    uint256 public valeur;

    // Q2.2: Updates the state variable
    function setValeur(uint256 nouvelleValeur) public {
        valeur = nouvelleValeur;
    }

    // Q2.3: View function that reads the stored value
    function getValeur() public view returns (uint256) {
        return valeur;
    }
}
```

---

### Q2.4 Compilation
- Compiled using Solidity compiler version `0.8.20+commit.a1b79de6`.
- Compilation completed with **0 errors and 0 warnings**.

---

### Q2.5 Environment Connection
In Remix's **Deploy & Run Transactions** tab:
- Environment selected: **Dev - Ganache Provider** (or **Custom - External HTTP Provider**).
- Web3 Provider Endpoint: `http://127.0.0.1:8545`.

---

### Q2.6 Contract Deployment
- **Deploying Account:** `0x15ac6d7f4e5c685babf0b0023ed0240d7e5b244c` (Account 0)
- **Deployed Contract Address:** `0x254c624cc2ba95d032b6346703cd52ac2d4c895d`
- **Initial Deployment Block Number:** Block `2` (after transaction `0xad66...`)

---

### Q2.7 Function Execution & Results
1. Executed `getValeur()` before update: returns `0`.
2. Executed transaction `setValeur(10)`: transaction mined successfully.
3. Executed `getValeur()` after update:
   - **Obtained Value:** `10`.

---

### Q2.8 Observation of Transactions & Blocks in Ganache
- **Deployment:** Produced **1 new transaction** and created **1 new block** (Block `2`).
- **Executing `setValeur(10)`:** Produced **1 new transaction** and created **1 new block** (Block `3`).
- **Total New Blocks & Transactions Observed:** **2 transactions and 2 blocks**.

---

### Q2.9 `getValeur()` Call vs. State-Changing Transaction
- **Did `getValeur()` produce a new transaction in Ganache?** **No**, the block number remained unchanged and no transaction receipt was generated.
- **Explanation:**
  - `getValeur()` is a **`view` function** that only reads storage without altering the state of the blockchain.
  - View calls are executed locally on the connected node via the `eth_call` JSON-RPC method. They do not require cryptographic signing, consensus, mining, or gas expenditure.
  - Conversely, `setValeur(10)` modifies contract storage (`valeur = nouvelleValeur`), requiring an on-chain transaction (`eth_sendTransaction`), digital signature, gas consumption, inclusion into a block, and state transition validation across all nodes.

---

## Part 3: Demonstration of Smart Contract Vulnerabilities

### A. Missing Access Control

#### Q3.1 Deploying `CoffreVulnerable` & Calling `modify(10)`
- Deployed from Account `(0)` (`0x15ac...`).
- Called `modify(10)` from Account `(0)`.
- Contract storage `valeur` updated to `10`.

#### Q3.2 Calling `modify(999)` from Account `(1)`
- Selected Account `(1)` (`0xa392...`) in Remix and called `modify(999)`.
- **Result:** The call **succeeded**, and `valeur` was overwritten to `999`.
- **Why?** The `modify` function was marked `public` with no authorization guard or sender check. Any account on the network can invoke it and overwrite the contract's critical state.

#### Q3.3 & Q3.4 Secured Implementation (`CoffreSecurise.sol`)
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CoffreSecurise {
    uint256 public valeur;
    // Q3.3: Owner state variable
    address public proprietaire;

    // Store deployer as the owner
    constructor() {
        proprietaire = msg.sender;
    }

    // Q3.4: Function with authorization check
    function modify(uint256 nouvelleValeur) public {
        require(msg.sender == proprietaire, "Access denied");
        valeur = nouvelleValeur;
    }
}
```

#### Q3.5 Testing `CoffreSecurise`
- **Test with Owner Account `(0)`:** Call `modify(50)` **succeeds**. Value is updated to `50`.
- **Test with Unauthorized Account `(1)`:** Call `modify(999)` **reverts** with status `0x0` and error message:
  ```text
  VM Exception while processing transaction: revert Access denied
  ```
- `valeur` remains protected at `50`.

#### Q3.6 Meaning of `msg.sender` & Purpose of `require()`
- **`msg.sender`:** Represents the immediate Ethereum address that initiated the current function call or transaction.
- **Security Role:** The `require(msg.sender == proprietaire, "Access denied")` statement enforces **authentication and authorization**. It prevents unauthorized external actors from tampering with restricted contract functions.

---

### B. Reentrancy Vulnerability

#### Q3.7 Risk of External Call Before Balance Update
In the vulnerable withdrawal pattern:
```solidity
(bool ok, ) = msg.sender.call{value: montant}("");
require(ok);
soldes[msg.sender] = 0;
```
- **The Risk:** When sending Ether via `call{value: montant}("")`, control flow is transferred to the receiving contract's `receive()` or `fallback()` function.
- If the receiver is a malicious contract, its `receive()` function can immediately call `retirer()` again **before** `soldes[msg.sender] = 0` is reached.
- Because the stored balance has not yet been zeroed, the requirement `require(montant > 0)` passes again, sending another batch of funds. This cycle repeats recursively until all contract funds or gas are exhausted.
- **Demonstration Result:** In our test (`test_reentrancy.js`), the attacker deposited 1 ETH and recursively drained the entire 5 ETH deposited by the victim, exiting with 6 ETH while the victim contract was left with 0 ETH.

#### Q3.8 Reducing the Vulnerability (The Simple Change)
Update the state **before** making the external call:
```solidity
uint256 montant = soldes[msg.sender];
require(montant > 0, "Solde insuffisant");

// Update state FIRST
soldes[msg.sender] = 0;

// Make external transfer SECOND
(bool ok, ) = msg.sender.call{value: montant}("");
require(ok, "Transfert echoue");
```
When an attacker re-enters `retirer()`, `soldes[msg.sender]` is already `0`, immediately aborting further recursive withdrawals.

#### Q3.9 General Rule: Checks-Effects-Interactions (CEI) Pattern
When developing smart contracts:
1. **Checks:** Validate all preconditions, parameters, and access controls (`require`, `revert`).
2. **Effects:** Apply all state changes internally (updating balances, setting flags, emitting events).
3. **Interactions:** Only after all state updates are complete, interact with external contracts or transfer Ether.
4. Additionally, use a mutex guard (e.g. OpenZeppelin's `ReentrancyGuard` with the `nonReentrant` modifier) for defense in depth.
