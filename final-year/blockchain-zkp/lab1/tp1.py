import hashlib
import json

# Exercise 0: Getting started with cryptographic hashing

def h(s: str) -> str:
    """Compute the SHA-256 hash of a string."""
    return hashlib.sha256(s.encode()).hexdigest()


# Exercise 1 & 2: Define Block class with Mining

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # We serialize index, data, previous_hash, nonce in this exact order
        serialized_data = json.dumps([self.index, self.data, self.previous_hash, self.nonce])
        return h(serialized_data)

    def mine(self, difficulty):
        target = "0" * difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()


# Exercise 3 & 4: Define Blockchain class with Validation

class Blockchain:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        genesis_block = Block(0, "Genesis Block", "0" * 64)
        genesis_block.mine(self.difficulty)
        self.blocks = [genesis_block]

    def add_block(self, data):
        prev_block = self.blocks[-1]
        new_block = Block(len(self.blocks), data, prev_block.hash)
        new_block.mine(self.difficulty)
        self.blocks.append(new_block)

    def display(self):
        for b in self.blocks:
            print(f"--- Block #{b.index} ---")
            print(f"  Index        : {b.index}")
            print(f"  Data         : {b.data}")
            print(f"  Previous Hash: {b.previous_hash}")
            print(f"  Nonce        : {b.nonce}")
            print(f"  Hash         : {b.hash}")

    def is_valid(self):
        if not self.blocks:
            return False

        target = "0" * self.difficulty

        for i, block in enumerate(self.blocks):
            # 1. Index must match its position in the list
            if block.index != i:
                return False

            # 2. Stored hash must match recalculated hash
            if block.hash != block.calculate_hash():
                return False

            # 3. Hash must satisfy difficulty condition (leading zeros)
            if not block.hash.startswith(target):
                return False

            # 4. First block convention checks
            if i == 0:
                if block.data != "Genesis Block" or block.previous_hash != "0" * 64:
                    return False
            # 5. Consecutive blocks linkage check
            else:
                prev_block = self.blocks[i - 1]
                if block.previous_hash != prev_block.hash:
                    return False

        return True


# Tests and Demonstrations for Lab Questions

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCISE 0: Cryptographic Hashing (SHA-256)")
    print("=" * 60)

    # Q0.1: Determinism check
    hash1 = h("blockchain")
    hash2 = h("blockchain")
    print(f"Q0.1 Determinism test: h('blockchain') == h('blockchain') -> {hash1 == hash2}")
    print(f"     Hash: {hash1}\n")

    # Q0.2: Avalanche effect
    h_upper = h("Blockchain")
    h_lower = h("blockchain")
    diff_chars = sum(c1 != c2 for c1, c2 in zip(h_upper, h_lower))
    print(f"Q0.2 Avalanche effect comparison:")
    print(f"     h('Blockchain'): {h_upper}")
    print(f"     h('blockchain'): {h_lower}")
    print(f"     Different characters: {diff_chars}/64 ({diff_chars / 64:.2%})\n")

    # Q0.3: Output length
    s1 = "a"
    s10 = "a" * 10
    s1000 = "a" * 1000
    print(f"Q0.3 Hash length test:")
    print(f"     len(h(1 char))    = {len(h(s1))} hex characters (256 bits)")
    print(f"     len(h(10 chars))   = {len(h(s10))} hex characters (256 bits)")
    print(f"     len(h(1000 chars)) = {len(h(s1000))} hex characters (256 bits)\n")

    print("=" * 60)
    print("EXERCISE 1: Block Class Testing")
    print("=" * 60)
    b0 = Block(0, "Genesis Block", "0" * 64)
    print(f"Q1.3 Initial block: Index={b0.index}, Nonce={b0.nonce}")
    print(f"     Stored hash: {b0.hash}")
    stored_h = b0.hash
    b0.nonce = 1
    recalculated_h = b0.calculate_hash()
    print(f"     After setting nonce=1:")
    print(f"     Recalculated hash: {recalculated_h}")
    print(f"     Stored hash      : {stored_h}")
    print(f"     Hashes match? -> {recalculated_h == stored_h}\n")

    print("=" * 60)
    print("EXERCISE 2: Mining and Proof-of-Work")
    print("=" * 60)
    # Q2.2: Mining with difficulty 2
    b_mine2 = Block(0, "Mining Test", "0" * 64)
    b_mine2.mine(difficulty=2)
    print(f"Q2.2 Mining with difficulty 2:")
    print(f"     Nonce found: {b_mine2.nonce}")
    print(f"     Hash       : {b_mine2.hash}")
    print(f"     Starts with '00'? -> {b_mine2.hash.startswith('00')}")
    print(f"Q2.3 Nonces tested for diff 2 (including 0): {b_mine2.nonce + 1}\n")

    # Q2.3: Mining with difficulty 3
    b_mine3 = Block(0, "Mining Test", "0" * 64)
    b_mine3.mine(difficulty=3)
    print(f"Q2.3 Mining with difficulty 3:")
    print(f"     Nonce found: {b_mine3.nonce}")
    print(f"     Hash       : {b_mine3.hash}")
    print(f"     Starts with '000'? -> {b_mine3.hash.startswith('000')}")
    print(f"     Nonces tested for diff 3 (including 0): {b_mine3.nonce + 1}\n")

    print("=" * 60)
    print("EXERCISE 3: Blockchain Class & Chain Construction")
    print("=" * 60)
    bc = Blockchain(difficulty=2)
    bc.add_block("Transaction 1: Alice -> Bob 5 BTC")
    bc.add_block("Transaction 2: Bob -> Charlie 2.5 BTC")
    bc.add_block("Transaction 3: Charlie -> Dave 1 BTC")
    print(f"Q3.4 Chain created with difficulty 2. Total blocks: {len(bc.blocks)}\n")
    bc.display()
    print()

    print("=" * 60)
    print("EXERCISE 4: Validation and Tamper Resistance")
    print("=" * 60)
    # Q4.3: Initial validity and tampering
    print(f"Q4.3 Initial blockchain validity: bc.is_valid() -> {bc.is_valid()}")
    print("     Modifying data in block 1: 'Hacked Transaction'...")
    bc.blocks[1].data = "Hacked Transaction: Alice -> Eve 100 BTC"
    print(f"     After data modification: bc.is_valid() -> {bc.is_valid()}\n")

    # Q4.4: Re-mining only block 1
    print("Q4.4 Re-mining only block 1...")
    bc.blocks[1].mine(bc.difficulty)
    print(f"     Block 1 re-mined hash: {bc.blocks[1].hash}")
    print(f"     Block 2 previous_hash: {bc.blocks[2].previous_hash}")
    print(f"     Is the chain valid now? bc.is_valid() -> {bc.is_valid()}")
    print(f"     Does Block 2 point to Block 1's new hash? -> {bc.blocks[2].previous_hash == bc.blocks[1].hash}")
    print("=" * 60)
