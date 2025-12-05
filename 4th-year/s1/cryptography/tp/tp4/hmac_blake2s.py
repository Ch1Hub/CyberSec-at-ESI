"""
HMAC-BLAKE2s Implementation
Message Authentication Code using BLAKE2s hash function
"""

from blake2s import BLAKE2s, blake2s


class HMAC_BLAKE2s:
    """
    HMAC (Hash-based Message Authentication Code) using BLAKE2s.
    
    HMAC-BLAKE2s(K, m) = BLAKE2s((K ⊕ opad) || BLAKE2s((K ⊕ ipad) || m))
    
    where:
        K = secret key
        m = message
        ipad = 0x36 repeated (inner padding)
        opad = 0x5c repeated (outer padding)
        || = concatenation
        ⊕ = XOR
    """
    
    # HMAC padding constants
    IPAD = 0x36  # Inner padding byte
    OPAD = 0x5C  # Outer padding byte
    BLOCK_SIZE = 64  # BLAKE2s block size in bytes
    
    def __init__(self, key, digest_size=32):
        """
        Initialize HMAC-BLAKE2s.
        
        Args:
            key: Secret key (bytes or string)
            digest_size: Output size in bytes (default 32 for 256 bits)
        """
        if isinstance(key, str):
            key = key.encode('utf-8')
        
        self.digest_size = digest_size
        
        # If key is longer than block size, hash it first
        if len(key) > self.BLOCK_SIZE:
            key = blake2s(key, digest_size=32)  # Hash to 32 bytes
        
        # Pad key to block size with zeros
        if len(key) < self.BLOCK_SIZE:
            key = key + b'\x00' * (self.BLOCK_SIZE - len(key))
        
        self.key = key
        
        # Compute K ⊕ ipad and K ⊕ opad
        self.key_ipad = bytes(b ^ self.IPAD for b in self.key)
        self.key_opad = bytes(b ^ self.OPAD for b in self.key)
        
        # Initialize inner hash
        self.inner_hasher = BLAKE2s(digest_size=32)  # Always use 256-bit for inner hash
        self.inner_hasher.update(self.key_ipad)
        
        self.finalized = False
    
    def update(self, data):
        """
        Add data to the message being authenticated.
        
        Args:
            data: bytes or string to add to message
        """
        if self.finalized:
            raise ValueError("Cannot update finalized HMAC")
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.inner_hasher.update(data)
    
    def finalize(self):
        """
        Finalize and compute the HMAC.
        
        Returns:
            bytes: HMAC digest
        """
        if self.finalized:
            raise ValueError("HMAC already finalized")
        
        self.finalized = True
        
        # Complete inner hash: BLAKE2s((K ⊕ ipad) || m)
        inner_hash = self.inner_hasher.digest()
        
        # Compute outer hash: BLAKE2s((K ⊕ opad) || inner_hash)
        outer_hasher = BLAKE2s(digest_size=self.digest_size)
        outer_hasher.update(self.key_opad)
        outer_hasher.update(inner_hash)
        
        return outer_hasher.digest()
    
    def digest(self):
        """Get the HMAC digest as bytes"""
        return self.finalize()
    
    def hexdigest(self):
        """Get the HMAC digest as hexadecimal string"""
        return self.digest().hex()


def hmac_blake2s(key, message, digest_size=32):
    """
    Compute HMAC-BLAKE2s in one call.
    
    Args:
        key: Secret key (bytes or string)
        message: Message to authenticate (bytes or string)
        digest_size: Output size in bytes (default 32 for 256 bits)
    
    Returns:
        bytes: HMAC digest
    
    Example:
        >>> mac = hmac_blake2s(b"secret_key", b"message")
        >>> print(mac.hex())
    """
    hmac = HMAC_BLAKE2s(key, digest_size)
    hmac.update(message)
    return hmac.digest()


def hmac_blake2s_hex(key, message, digest_size=32):
    """
    Compute HMAC-BLAKE2s and return as hex string.
    
    Args:
        key: Secret key (bytes or string)
        message: Message to authenticate (bytes or string)
        digest_size: Output size in bytes (default 32 for 256 bits)
    
    Returns:
        str: HMAC digest as hexadecimal string
    
    Example:
        >>> mac_hex = hmac_blake2s_hex("secret_key", "message")
        >>> print(mac_hex)
    """
    return hmac_blake2s(key, message, digest_size).hex()


def verify_hmac(key, message, expected_mac, digest_size=32):
    """
    Verify an HMAC-BLAKE2s authentication tag.
    Uses constant-time comparison to prevent timing attacks.
    
    Args:
        key: Secret key (bytes or string)
        message: Message to verify (bytes or string)
        expected_mac: Expected HMAC value (bytes or hex string)
        digest_size: Output size in bytes (default 32 for 256 bits)
    
    Returns:
        bool: True if MAC is valid, False otherwise
    
    Example:
        >>> mac = hmac_blake2s(b"key", b"message")
        >>> verify_hmac(b"key", b"message", mac)
        True
    """
    # Compute HMAC
    computed_mac = hmac_blake2s(key, message, digest_size)
    
    # Convert expected_mac to bytes if it's a hex string
    if isinstance(expected_mac, str):
        expected_mac = bytes.fromhex(expected_mac)
    
    # Constant-time comparison to prevent timing attacks
    if len(computed_mac) != len(expected_mac):
        return False
    
    result = 0
    for a, b in zip(computed_mac, expected_mac):
        result |= a ^ b
    
    return result == 0


if __name__ == "__main__":
    print("HMAC-BLAKE2s Implementation Test")
    print("=" * 70)
    
    # Test 1: Basic HMAC
    print("\nTest 1: Basic HMAC")
    key = b"secret_key"
    message = b"The quick brown fox jumps over the lazy dog"
    mac = hmac_blake2s_hex(key, message)
    print(f"Key:     {key}")
    print(f"Message: {message}")
    print(f"HMAC:    {mac}")
    
    # Test 2: Empty message
    print("\nTest 2: Empty message")
    mac_empty = hmac_blake2s_hex(b"key", b"")
    print(f"Key:     b'key'")
    print(f"Message: b''")
    print(f"HMAC:    {mac_empty}")
    
    # Test 3: Long key (longer than block size)
    print("\nTest 3: Long key (> 64 bytes)")
    long_key = b"x" * 100
    mac_long = hmac_blake2s_hex(long_key, b"message")
    print(f"Key:     b'{'x' * 100}' (100 bytes)")
    print(f"Message: b'message'")
    print(f"HMAC:    {mac_long}")
    
    # Test 4: Incremental update
    print("\nTest 4: Incremental hashing")
    hmac1 = HMAC_BLAKE2s(b"key")
    hmac1.update(b"Hello, ")
    hmac1.update(b"World!")
    mac_incremental = hmac1.hexdigest()
    
    mac_one_shot = hmac_blake2s_hex(b"key", b"Hello, World!")
    
    print(f"Incremental: {mac_incremental}")
    print(f"One-shot:    {mac_one_shot}")
    print(f"Match:       {mac_incremental == mac_one_shot}")
    
    # Test 5: Verification
    print("\nTest 5: HMAC Verification")
    key = b"authentication_key"
    message = b"Important message"
    mac = hmac_blake2s(key, message)
    
    valid = verify_hmac(key, message, mac)
    print(f"Message:        {message}")
    print(f"MAC:            {mac.hex()}")
    print(f"Verification:   {valid}")
    
    # Try with wrong key
    wrong_key_valid = verify_hmac(b"wrong_key", message, mac)
    print(f"Wrong key:      {wrong_key_valid}")
    
    # Try with tampered message
    tampered_valid = verify_hmac(key, b"Tampered message", mac)
    print(f"Tampered msg:   {tampered_valid}")
    
    # Test 6: Different digest sizes
    print("\nTest 6: Different digest sizes")
    for size in [16, 20, 24, 28, 32]:
        mac = hmac_blake2s_hex(b"key", b"message", digest_size=size)
        print(f"{size*8}-bit: {mac}")
    
    print("\n" + "=" * 70)
    print("All tests completed!")
