"""
HMAC-BLAKE2s Implementation
HMAC (Hash-based Message Authentication Code) using BLAKE2s
"""

from blake2s import blake2s


def hmac_blake2s(key, message):
    """
    HMAC-BLAKE2s implementation
    
    HMAC-BLAKE2(K, M) = BLAKE2((K ⊕ opad) || BLAKE2((K ⊕ ipad) || M))
    
    Args:
        key: bytes or string - secret key
        message: bytes or string - message to authenticate
    
    Returns:
        bytes: 32-byte authentication tag
    """
    # Convert to bytes if needed
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    # BLAKE2s block size is 64 bytes
    block_size = 64
    
    # Pad definitions
    ipad = bytes([0x36] * block_size)
    opad = bytes([0x5c] * block_size)
    
    # If key is longer than block size, hash it first
    if len(key) > block_size:
        key = blake2s(key)
    
    # Pad key to block size
    if len(key) < block_size:
        key = key + bytes(block_size - len(key))
    
    # Compute inner hash: BLAKE2((K ⊕ ipad) || M)
    inner_key_pad = bytes([k ^ i for k, i in zip(key, ipad)])
    inner_hash = blake2s(inner_key_pad + message)
    
    # Compute outer hash: BLAKE2((K ⊕ opad) || inner_hash)
    outer_key_pad = bytes([k ^ o for k, o in zip(key, opad)])
    hmac = blake2s(outer_key_pad + inner_hash)
    
    return hmac


def hmac_blake2s_hex(key, message):
    """
    HMAC-BLAKE2s implementation returning hex string
    
    Args:
        key: bytes or string - secret key
        message: bytes or string - message to authenticate
    
    Returns:
        str: hexadecimal authentication tag
    """
    return hmac_blake2s(key, message).hex()


def verify_hmac(key, message, tag):
    """
    Verify HMAC tag
    
    Args:
        key: bytes or string - secret key
        message: bytes or string - message to verify
        tag: bytes - expected HMAC tag
    
    Returns:
        bool: True if valid, False otherwise
    """
    if isinstance(tag, str):
        tag = bytes.fromhex(tag)
    
    computed_tag = hmac_blake2s(key, message)
    
    # Constant-time comparison to prevent timing attacks
    return len(tag) == len(computed_tag) and sum(a != b for a, b in zip(tag, computed_tag)) == 0


if __name__ == "__main__":
    # Test HMAC-BLAKE2s
    print("Testing HMAC-BLAKE2s implementation:")
    print()
    
    # Test 1: Simple message
    key1 = b"secret_key"
    msg1 = b"Hello, World!"
    tag1 = hmac_blake2s(key1, msg1)
    print(f"Key: {key1}")
    print(f"Message: {msg1}")
    print(f"HMAC: {tag1.hex()}")
    print()
    
    # Test 2: Verification
    print("Testing verification:")
    print(f"Valid tag: {verify_hmac(key1, msg1, tag1)}")
    print(f"Invalid tag: {verify_hmac(key1, b'Wrong message', tag1)}")
    print()
    
    # Test 3: Longer key and message
    key2 = b"This is a much longer secret key for testing purposes"
    msg2 = b"The quick brown fox jumps over the lazy dog"
    tag2 = hmac_blake2s(key2, msg2)
    print(f"Key: {key2}")
    print(f"Message: {msg2}")
    print(f"HMAC: {tag2.hex()}")
