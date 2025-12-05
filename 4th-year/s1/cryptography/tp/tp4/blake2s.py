"""
BLAKE2s-256 Hash Function Implementation
Optimized cryptographic hash function producing 256-bit output
"""

import struct
import hashlib

class BLAKE2s:
    """
    BLAKE2s-256 hash function implementation.
    Produces 256-bit (32-byte) hash values.
    Optimized for 8-32 bit platforms.
    """
    
    # BLAKE2s initialization vector (IV) - first 32 bits of fractional parts of sqrt(primes)
    IV = [
        0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
        0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19
    ]
    
    # BLAKE2s permutation table (sigma)
    SIGMA = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
        [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
        [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
        [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
        [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
        [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
        [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
        [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
        [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0]
    ]
    
    def __init__(self, digest_size=32, key=b''):
        """
        Initialize BLAKE2s hasher.
        
        Args:
            digest_size: Output size in bytes (default 32 for 256 bits)
            key: Optional key for keyed hashing (0-32 bytes)
        """
        if not (1 <= digest_size <= 32):
            raise ValueError("Digest size must be between 1 and 32 bytes")
        if len(key) > 32:
            raise ValueError("Key must be at most 32 bytes")
        
        self.digest_size = digest_size
        self.key = key
        
        # Initialize hash state
        self.h = list(self.IV)
        
        # XOR h[0] with parameter block
        # 0x01010000 XOR digest_size XOR (key_length << 8)
        self.h[0] ^= 0x01010000 ^ self.digest_size ^ (len(key) << 8)
        
        self.buffer = b''
        self.t = [0, 0]  # 128-bit counter (low, high)
        self.finalized = False
        
        # If keyed, process key as first block
        if key:
            block = key + b'\x00' * (64 - len(key))
            self.buffer = block
    
    @staticmethod
    def rotr32(x, n):
        """Rotate right operation for 32-bit integers"""
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF
    
    def G(self, v, a, b, c, d, x, y):
        """
        BLAKE2s G mixing function.
        Mixes four words using two message words.
        """
        v[a] = (v[a] + v[b] + x) & 0xFFFFFFFF
        v[d] = self.rotr32(v[d] ^ v[a], 16)
        v[c] = (v[c] + v[d]) & 0xFFFFFFFF
        v[b] = self.rotr32(v[b] ^ v[c], 12)
        v[a] = (v[a] + v[b] + y) & 0xFFFFFFFF
        v[d] = self.rotr32(v[d] ^ v[a], 8)
        v[c] = (v[c] + v[d]) & 0xFFFFFFFF
        v[b] = self.rotr32(v[b] ^ v[c], 7)
    
    def compress(self, block, f=False):
        """
        BLAKE2s compression function.
        Processes one 64-byte block.
        
        Args:
            block: 64 bytes of input
            f: Final block flag
        """
        # Parse block into 16 message words (little-endian)
        m = list(struct.unpack('<16I', block))
        
        # Initialize working vector
        v = list(self.h) + list(self.IV)
        
        # XOR in the counter and final flag
        v[12] ^= self.t[0]
        v[13] ^= self.t[1]
        if f:
            v[14] ^= 0xFFFFFFFF
        
        # 10 rounds of mixing
        for r in range(10):
            s = self.SIGMA[r]
            
            # Column step
            self.G(v, 0, 4,  8, 12, m[s[0]], m[s[1]])
            self.G(v, 1, 5,  9, 13, m[s[2]], m[s[3]])
            self.G(v, 2, 6, 10, 14, m[s[4]], m[s[5]])
            self.G(v, 3, 7, 11, 15, m[s[6]], m[s[7]])
            
            # Diagonal step
            self.G(v, 0, 5, 10, 15, m[s[8]],  m[s[9]])
            self.G(v, 1, 6, 11, 12, m[s[10]], m[s[11]])
            self.G(v, 2, 7,  8, 13, m[s[12]], m[s[13]])
            self.G(v, 3, 4,  9, 14, m[s[14]], m[s[15]])
        
        # XOR working vector into hash state
        for i in range(8):
            self.h[i] ^= v[i] ^ v[i + 8]
    
    def increment_counter(self, inc):
        """Increment the 128-bit counter"""
        self.t[0] = (self.t[0] + inc) & 0xFFFFFFFF
        if self.t[0] < inc:
            self.t[1] = (self.t[1] + 1) & 0xFFFFFFFF
    
    def update(self, data):
        """
        Add data to be hashed.
        
        Args:
            data: bytes, bytearray, or string to hash
        """
        if self.finalized:
            raise ValueError("Cannot update finalized hash")
        
        # Convert string to bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.buffer += data
        
        # Process complete 64-byte blocks
        while len(self.buffer) >= 64:
            block = self.buffer[:64]
            self.buffer = self.buffer[64:]
            self.increment_counter(64)
            self.compress(block, False)
    
    def finalize(self):
        """
        Finalize the hash and return the digest.
        
        Returns:
            bytes: Hash digest
        """
        if self.finalized:
            raise ValueError("Hash already finalized")
        
        self.finalized = True
        
        # Pad remaining buffer with zeros
        buf_len = len(self.buffer)
        self.buffer += b'\x00' * (64 - buf_len)
        
        # Update counter with remaining bytes
        self.increment_counter(buf_len)
        
        # Process final block
        self.compress(self.buffer, True)
        
        # Output hash (little-endian)
        output = b''.join(struct.pack('<I', word) for word in self.h)
        return output[:self.digest_size]
    
    def digest(self):
        """Get the hash digest as bytes"""
        return self.finalize()
    
    def hexdigest(self):
        """Get the hash digest as hexadecimal string"""
        return self.digest().hex()


def blake2s(data, digest_size=32, key=b''):
    """
    Convenience function to hash data in one call.
    
    Args:
        data: bytes, bytearray, or string to hash
        digest_size: Output size in bytes (default 32 for 256 bits)
        key: Optional key for keyed hashing
    
    Returns:
        bytes: Hash digest
    """
    hasher = BLAKE2s(digest_size=digest_size, key=key)
    hasher.update(data)
    return hasher.digest()


def blake2s_hex(data, digest_size=32, key=b''):
    """
    Convenience function to hash data and return hex string.
    
    Args:
        data: bytes, bytearray, or string to hash
        digest_size: Output size in bytes (default 32 for 256 bits)
        key: Optional key for keyed hashing
    
    Returns:
        str: Hexadecimal hash string
    """
    return blake2s(data, digest_size, key).hex()


if __name__ == "__main__":
    # Basic test
    print("BLAKE2s-256 Implementation Test")
    print("=" * 64)
    
    # Test vector from RFC 7693
    test_data = b"THE QUIVK NOTEN OFX JUMPD OBRT YJR LWZY DOG"
    result = blake2s_hex(test_data)
    expected = hashlib.blake2s(test_data).hexdigest()
    
    print(f"Input:    {test_data}")
    print(f"Output:   {result}")
    print(f"Expected: {expected}")
    print(f"Match:    {result == expected}")
    