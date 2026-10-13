# TP1: Introduction to Blockchain - Lab Report

**Student:** Chikhaoui Youcef Chihab Eddine  
**Module:** Emergent Security Technologies  
**School:** ESI-SBA  
**Academic Year:** 2026–2027  

---

### Exercise 0: Getting started with cryptographic hashing

**Q0.1 Check determinism: does the same text, supplied twice, produce the same hash?**  
Yes. When I tested `h("blockchain")` two times, I got the exact same hash:  
`ef7797e13d3a75526946a3bcf00daec9fc9c9c4d51ddc7cc5df888f74dd434d1`  
Hash functions are deterministic, so the same input always gives the same output.

**Q0.2 Calculate h("Blockchain") and h("blockchain"). What proportion of the characters changes?**  
- `h("Blockchain")` = `625da44e4eaf58d61cf048d168aa6f5e492dea166d8bb54ec06c30de07db57e1`  
- `h("blockchain")` = `ef7797e13d3a75526946a3bcf00daec9fc9c9c4d51ddc7cc5df888f74dd434d1`  

Just by changing the first letter from uppercase 'B' to lowercase 'b', 62 out of the 64 characters changed (about 97%). This shows the avalanche effect: even a tiny change in the input completely changes the hash.

**Q0.3 Test strings of 1, 10 and 1000 characters. What do you notice about the length of the hashes?**  
- String of 1 char: 64 characters  
- String of 10 chars: 64 characters  
- String of 1000 chars: 64 characters  

No matter how short or long the input text is, the SHA-256 hash always has a fixed length of 64 hexadecimal characters (256 bits).

---

### Exercise 1: Define the Block class

**Q1.1 & Q1.2 Implementation:**  
I implemented the `Block` class in `tp1.py`. In `__init__`, I saved `index`, `data`, `previous_hash`, set `nonce = 0`, and called `calculate_hash()`. In `calculate_hash()`, I used `json.dumps()` on `[self.index, self.data, self.previous_hash, self.nonce]` and returned `h()`.

**Q1.3 Genesis block test and nonce modification:**  
I created `b0 = Block(0, "Genesis Block", "0" * 64)`.  
Its initial hash was: `cd97ad6a6c52c35e563fad29a543769ff0947b1f186a703933a35afe1e8eedc2`.  
Then I changed `b0.nonce = 1` and recalculated the hash:  
`b34ec5bea09e14212c716f9d87d4ea0ee225158d8b3cbee342ecea8b1a0de047`.  
The recalculated hash is completely different from the stored hash because changing the nonce changes the block data.

**Q1.4 Questions:**  
- **Why is the hash attribute excluded from the calculation?**  
Because we cannot hash the hash itself while we are calculating it. It would cause a loop. The hash is the result of hashing the block's contents.  
- **What do the first block's 64 zeros represent?**  
The first block is the Genesis block, so there is no previous block before it. The 64 zeros are just a placeholder for the previous hash.

---

### Exercise 2: Add mining to a block

**Q2.1 Implementation:**  
I added the `mine(self, difficulty)` method. It starts at `nonce = 0` and increments it by 1 in a `while` loop until `self.hash.startswith("0" * difficulty)`.

**Q2.2 Test mining with difficulty = 2:**  
I created `Block(0, "Mining Test", "0" * 64)` and called `.mine(2)`.  
- Nonce found: `571`  
- Hash: `008f3a04d8dc53d643918089aca9eb6f671a75f75eb2308d985f6f42b81aac89`  
Yes, the hash starts with `00`.

**Q2.3 Nonces tested and comparison with difficulty = 3:**  
- For difficulty 2: 572 nonces tested (from 0 to 571).  
- For difficulty 3: Nonce found was `870`, so 871 nonces were tested. Hash: `00054e0b40245df44687127a8ba4f1734ca6d282c747bb9fcb9557a14d03d058`.  
With difficulty 3, it took more attempts because finding 3 leading zeros is harder than finding 2.

**Q2.4 What if the nonce never changed?**  
Since the hash function is deterministic, if the nonce stays the same, the hash will never change. If the first hash doesn't start with the required zeros, the code will get stuck in an infinite loop forever.

---

### Exercise 3: Define the Blockchain class

**Q3.1, Q3.2 & Q3.3 Implementation:**  
I created the `Blockchain` class:  
- `__init__` sets `self.difficulty`, creates the Genesis block, mines it, and puts it in `self.blocks`.  
- `add_block` takes the hash of the last block, creates a new block, mines it with `self.difficulty`, and appends it.  
- `display` prints the index, data, previous hash, nonce, and hash for each block.

**Q3.4 Testing with difficulty 2 and adding 3 blocks:**  
I created `bc = Blockchain(2)` and added 3 blocks.  
The chain contains **4 blocks** in total (the Genesis block + the 3 new blocks).

**Q3.5 Link between blocks 0 and 1 & why add_block() doesn't need difficulty:**  
- Block 1's `previous_hash` matches Block 0's `hash`. That is how they are linked together.  
- `add_block()` does not need a difficulty parameter because the difficulty is already saved in the blockchain object (`self.difficulty`).

---

### Exercise 4: Validate and test the simulation

**Q4.1 & Q4.2 Implementation:**  
In `is_valid(self)`, I checked:
1. That the list of blocks is not empty.
2. For each block: `block.index == i`.
3. `block.hash == block.calculate_hash()` (the data wasn't modified).
4. `block.hash.startswith("0" * self.difficulty)` (the proof of work is valid).
5. For block 0: data is `"Genesis Block"` and previous hash is 64 zeros.
6. For other blocks: `block.previous_hash == self.blocks[i - 1].hash`.

**Q4.3 Tampering with block 1:**  
- At first, `bc.is_valid()` returned `True`.  
- After changing `bc.blocks[1].data = "Hacked Transaction..."`, `bc.is_valid()` returned `False`.  
*Explanation:* Changing the data changed the block's calculated hash. Since the stored hash didn't match the new calculated hash anymore, the validation failed.

**Q4.4 Re-mining only block 1:**  
I re-mined block 1 using `bc.blocks[1].mine(bc.difficulty)`.  
- Is the chain valid? **No, it is still False.**  
- *Why?* Because Block 1 now has a new hash, but Block 2's `previous_hash` is still pointing to Block 1's old hash. To make the chain valid again, an attacker would have to re-mine Block 1 AND Block 2 AND all the blocks that come after it.
