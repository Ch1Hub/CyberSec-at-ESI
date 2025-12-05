"""
Test script for Authenticated File Encryption System
"""

import os
from file_encryption import AuthenticatedFileEncryption


def test_encryption_system():
    """Test the encryption/decryption system"""
    
    encryptor = AuthenticatedFileEncryption()
    
    print("=" * 70)
    print("Testing Authenticated File Encryption System")
    print("=" * 70)
    
    # Create test file
    test_file = "test_file.txt"
    encrypted_file_cbc = "test_encrypted_cbc.bin"
    encrypted_file_ctr = "test_encrypted_ctr.bin"
    decrypted_file_cbc = "test_decrypted_cbc.txt"
    decrypted_file_ctr = "test_decrypted_ctr.txt"
    
    # Create test content
    test_content = b"This is a secret message that needs to be encrypted!\nMultiple lines test.\n"
    with open(test_file, 'wb') as f:
        f.write(test_content)
    
    password = "MySecurePassword123"
    
    # Test 1: CBC Mode
    print("\n" + "=" * 70)
    print("Test 1: CBC Mode Encryption/Decryption")
    print("=" * 70)
    
    print("\nEncrypting with CBC mode...")
    metadata_enc = encryptor.encrypt_file(test_file, encrypted_file_cbc, password, 'CBC')
    print(f"✓ Encryption successful")
    print(f"  Mode: {metadata_enc['mode']}")
    print(f"  Original size: {metadata_enc['input_size']} bytes")
    print(f"  Encrypted size: {metadata_enc['output_size']} bytes")
    print(f"  HMAC Tag: {metadata_enc['tag'][:32]}...")
    
    print("\nDecrypting CBC encrypted file...")
    metadata_dec = encryptor.decrypt_file(encrypted_file_cbc, decrypted_file_cbc, password)
    print(f"✓ Decryption successful")
    print(f"  Mode: {metadata_dec['mode']}")
    print(f"  Decrypted size: {metadata_dec['output_size']} bytes")
    print(f"  Verified: {metadata_dec['verified']}")
    
    # Verify content
    with open(decrypted_file_cbc, 'rb') as f:
        decrypted_content = f.read()
    
    if decrypted_content == test_content:
        print("✓ Content verification: PASSED")
    else:
        print("✗ Content verification: FAILED")
    
    # Test 2: CTR Mode
    print("\n" + "=" * 70)
    print("Test 2: CTR Mode Encryption/Decryption")
    print("=" * 70)
    
    print("\nEncrypting with CTR mode...")
    metadata_enc = encryptor.encrypt_file(test_file, encrypted_file_ctr, password, 'CTR')
    print(f"✓ Encryption successful")
    print(f"  Mode: {metadata_enc['mode']}")
    print(f"  Original size: {metadata_enc['input_size']} bytes")
    print(f"  Encrypted size: {metadata_enc['output_size']} bytes")
    print(f"  HMAC Tag: {metadata_enc['tag'][:32]}...")
    
    print("\nDecrypting CTR encrypted file...")
    metadata_dec = encryptor.decrypt_file(encrypted_file_ctr, decrypted_file_ctr, password)
    print(f"✓ Decryption successful")
    print(f"  Mode: {metadata_dec['mode']}")
    print(f"  Decrypted size: {metadata_dec['output_size']} bytes")
    print(f"  Verified: {metadata_dec['verified']}")
    
    # Verify content
    with open(decrypted_file_ctr, 'rb') as f:
        decrypted_content = f.read()
    
    if decrypted_content == test_content:
        print("✓ Content verification: PASSED")
    else:
        print("✗ Content verification: FAILED")
    
    # Test 3: Wrong Password
    print("\n" + "=" * 70)
    print("Test 3: Wrong Password (Should Fail)")
    print("=" * 70)
    
    try:
        print("\nAttempting decryption with wrong password...")
        encryptor.decrypt_file(encrypted_file_cbc, "temp.txt", "WrongPassword")
        print("✗ SECURITY ISSUE: Decryption should have failed!")
    except ValueError as e:
        print(f"✓ Correctly rejected: {e}")
    
    # Test 4: Tampered File
    print("\n" + "=" * 70)
    print("Test 4: Tampered File (Should Fail)")
    print("=" * 70)
    
    # Tamper with encrypted file
    tampered_file = "tampered.bin"
    with open(encrypted_file_cbc, 'rb') as f:
        data = bytearray(f.read())
    
    # Flip a bit in the ciphertext
    data[50] ^= 0xFF
    
    with open(tampered_file, 'wb') as f:
        f.write(data)
    
    try:
        print("\nAttempting decryption of tampered file...")
        encryptor.decrypt_file(tampered_file, "temp.txt", password)
        print("✗ SECURITY ISSUE: Should have detected tampering!")
    except ValueError as e:
        print(f"✓ Tampering detected: {e}")
    
    # Cleanup
    print("\n" + "=" * 70)
    print("Cleaning up test files...")
    for f in [decrypted_file_cbc, decrypted_file_ctr, tampered_file]:
        if os.path.exists(f):
            os.remove(f)
    
    print("\n" + "=" * 70)
    print("All tests completed!")
    print("=" * 70)
    
    print("\nEncrypted files created:")
    print(f"  - {encrypted_file_cbc} (CBC mode)")
    print(f"  - {encrypted_file_ctr} (CTR mode)")
    print("\nYou can decrypt them using file_encryption.py")


if __name__ == "__main__":
    test_encryption_system()
