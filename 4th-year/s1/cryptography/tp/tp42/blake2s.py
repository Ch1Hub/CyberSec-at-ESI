"""
BLAKE2s Implementation
A cryptographic hash function that produces 256-bit outputs
"""

import struct

# BLAKE2s initialization vectors (first 32 bits of fractional parts of square roots of first 8 primes)
IV = [
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19
]

# BLAKE2s sigma (message schedule permutation)
SIGMA = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [14, 10, 4, 8, 9, 15, 6, 1, 12, 0, 2, 11, 7, 13, 5, 3],
    [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
    [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
    [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
    [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
    [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
    [13, 11, 10, 7, 4, 3, 15, 2, 5, 8, 0, 1, 6, 14, 9, 12],
    [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
    [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0]
]


def rotr32(x, n):
    """Rotate right for 32-bit integers"""
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF


def G(v, a, b, c, d, x, y):
    """BLAKE2s mixing function G"""
    v[a] = (v[a] + v[b] + x) & 0xFFFFFFFF
    v[d] = rotr32(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & 0xFFFFFFFF
    v[b] = rotr32(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & 0xFFFFFFFF
    v[d] = rotr32(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & 0xFFFFFFFF
    v[b] = rotr32(v[b] ^ v[c], 7)


def compress(h, chunk, t, f):
    """BLAKE2s compression function"""
    # Initialize working variables
    v = [0] * 16
    v[0:8] = h[0:8]
    v[8:16] = IV[0:8]
    
    v[12] ^= (t & 0xFFFFFFFF)
    v[13] ^= (t >> 32)
    
    if f:
        v[14] ^= 0xFFFFFFFF
    
    # Parse message block
    m = list(struct.unpack('<16I', chunk))
    
    # 10 rounds
    for i in range(10):
        s = SIGMA[i]
        G(v, 0, 4, 8, 12, m[s[0]], m[s[1]])
        G(v, 1, 5, 9, 13, m[s[2]], m[s[3]])
        G(v, 2, 6, 10, 14, m[s[4]], m[s[5]])
        G(v, 3, 7, 11, 15, m[s[6]], m[s[7]])
        G(v, 0, 5, 10, 15, m[s[8]], m[s[9]])
        G(v, 1, 6, 11, 12, m[s[10]], m[s[11]])
        G(v, 2, 7, 8, 13, m[s[12]], m[s[13]])
        G(v, 3, 4, 9, 14, m[s[14]], m[s[15]])
    
    # Update hash state
    for i in range(8):
        h[i] ^= v[i] ^ v[i + 8]


def blake2s(data, digest_size=32):
    """
    BLAKE2s hash function
    
    Args:
        data: bytes or string to hash
        digest_size: output size in bytes (default 32 for 256 bits)
    
    Returns:
        bytes: hash digest
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Initialize state
    h = IV.copy()
    h[0] ^= 0x01010000 ^ (digest_size & 0xFF)
    
    # Process message
    data_len = len(data)
    chunks = []
    
    # Split into 64-byte chunks
    for i in range(0, len(data), 64):
        chunks.append(data[i:i+64])
    
    # Process all but last chunk
    t = 0
    for i in range(len(chunks) - 1):
        t += 64
        compress(h, chunks[i].ljust(64, b'\x00'), t, False)
    
    # Process last chunk
    if chunks:
        last_chunk = chunks[-1]
        t += len(last_chunk)
        compress(h, last_chunk.ljust(64, b'\x00'), t, True)
    else:
        # Empty message
        compress(h, b'\x00' * 64, 0, True)
    
    # Produce output
    return struct.pack('<8I', *h)[:digest_size]


def blake2s_hex(data, digest_size=32):
    """
    BLAKE2s hash function returning hex string
    
    Args:
        data: bytes or string to hash
        digest_size: output size in bytes (default 32 for 256 bits)
    
    Returns:
        str: hexadecimal hash digest
    """
    return blake2s(data, digest_size).hex()


if __name__ == "__main__":
    # Test vectors
    print("Testing BLAKE2s implementation:")
    print()
    
    # Test 1: Empty string
    test1 = blake2s(b"")
    print(f"blake2s('') = {test1.hex()}")
    
    # Test 2: "abc"
    test2 = blake2s(b"abc")
    print(f"blake2s('abc') = {test2.hex()}")
    
    # Test 3: Longer message
    test3 = blake2s(b"The quick brown fox jumps over the lazy dog")
    print(f"blake2s('The quick brown fox jumps over the lazy dog') = {test3.hex()}")
    
    # Test 4: Random text
    test4 = blake2s("Hello, World! This is a test of BLAKE2s.")
    print(f"blake2s('Hello, World! This is a test of BLAKE2s.') = {test4.hex()}")
