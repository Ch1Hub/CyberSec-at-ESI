"""
File Encryption/Decryption Module
Supports CBC and CTR modes with BLAKE2s-derived keys
"""

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from blake2s import blake2s
from hmac_blake2s import hmac_blake2s, verify_hmac
import struct


class FileEncryptor:
    """Handles file encryption with CBC or CTR mode"""
    
    AES_BLOCK_SIZE = 16  # AES block size is 128 bits (16 bytes)
    
    def __init__(self):
        pass
    
    def derive_key(self, password):
        """
        Derive encryption key from password using BLAKE2s
        
        Args:
            password: str or bytes - user password
        
        Returns:
            bytes: 32-byte encryption key
        """
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        # Use BLAKE2s to derive a 256-bit (32-byte) key
        key = blake2s(password, digest_size=32)
        return key
    
    def encrypt_file_cbc(self, input_file, output_file, password):
        """
        Encrypt file using AES-CBC mode
        
        Args:
            input_file: str - path to file to encrypt
            output_file: str - path to save encrypted file
            password: str - encryption password
        
        Returns:
            bool: True if successful
        """
        # Derive key from password
        key = self.derive_key(password)
        
        # Generate random IV
        iv = get_random_bytes(self.AES_BLOCK_SIZE)
        
        # Read plaintext file
        with open(input_file, 'rb') as f:
            plaintext = f.read()
        
        # Encrypt using AES-CBC
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, self.AES_BLOCK_SIZE))
        
        # Calculate HMAC tag for authentication
        # Tag is computed over: mode || IV || ciphertext
        mode_byte = b'CBC'
        authenticated_data = mode_byte + iv + ciphertext
        tag = hmac_blake2s(key, authenticated_data)
        
        # Save encrypted file with format:
        # [mode (3 bytes)] [IV (16 bytes)] [tag (32 bytes)] [ciphertext]
        with open(output_file, 'wb') as f:
            f.write(mode_byte)
            f.write(iv)
            f.write(tag)
            f.write(ciphertext)
        
        return True
    
    def encrypt_file_ctr(self, input_file, output_file, password):
        """
        Encrypt file using AES-CTR mode
        
        Args:
            input_file: str - path to file to encrypt
            output_file: str - path to save encrypted file
            password: str - encryption password
        
        Returns:
            bool: True if successful
        """
        # Derive key from password
        key = self.derive_key(password)
        
        # Generate random nonce (IV for CTR mode)
        nonce = get_random_bytes(self.AES_BLOCK_SIZE // 2)  # 8 bytes for CTR
        
        # Read plaintext file
        with open(input_file, 'rb') as f:
            plaintext = f.read()
        
        # Encrypt using AES-CTR
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        ciphertext = cipher.encrypt(plaintext)
        
        # Calculate HMAC tag for authentication
        # Tag is computed over: mode || nonce || ciphertext
        mode_byte = b'CTR'
        authenticated_data = mode_byte + nonce + ciphertext
        tag = hmac_blake2s(key, authenticated_data)
        
        # Save encrypted file with format:
        # [mode (3 bytes)] [nonce (8 bytes)] [tag (32 bytes)] [ciphertext]
        with open(output_file, 'wb') as f:
            f.write(mode_byte)
            f.write(nonce)
            f.write(tag)
            f.write(ciphertext)
        
        return True
    
    def decrypt_file(self, input_file, output_file, password):
        """
        Decrypt file (auto-detects mode from file header)
        
        Args:
            input_file: str - path to encrypted file
            output_file: str - path to save decrypted file
            password: str - decryption password
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Derive key from password
        key = self.derive_key(password)
        
        # Read encrypted file
        with open(input_file, 'rb') as f:
            # Read mode (3 bytes)
            mode = f.read(3)
            
            if mode == b'CBC':
                # Read IV (16 bytes)
                iv = f.read(self.AES_BLOCK_SIZE)
                # Read tag (32 bytes)
                tag = f.read(32)
                # Read ciphertext
                ciphertext = f.read()
                
                # Verify HMAC
                authenticated_data = mode + iv + ciphertext
                if not verify_hmac(key, authenticated_data, tag):
                    return False, "The file is corrupted or the password is wrong"
                
                # Decrypt
                try:
                    cipher = AES.new(key, AES.MODE_CBC, iv)
                    plaintext = unpad(cipher.decrypt(ciphertext), self.AES_BLOCK_SIZE)
                except Exception as e:
                    return False, "Decryption failed: " + str(e)
                
            elif mode == b'CTR':
                # Read nonce (8 bytes)
                nonce = f.read(8)
                # Read tag (32 bytes)
                tag = f.read(32)
                # Read ciphertext
                ciphertext = f.read()
                
                # Verify HMAC
                authenticated_data = mode + nonce + ciphertext
                if not verify_hmac(key, authenticated_data, tag):
                    return False, "The file is corrupted or the password is wrong"
                
                # Decrypt
                try:
                    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
                    plaintext = cipher.decrypt(ciphertext)
                except Exception as e:
                    return False, "Decryption failed: " + str(e)
            else:
                return False, f"Unknown encryption mode: {mode}"
        
        # Save decrypted file
        with open(output_file, 'wb') as f:
            f.write(plaintext)
        
        return True, "File decrypted successfully"


if __name__ == "__main__":
    # Test encryption/decryption
    encryptor = FileEncryptor()
    
    # Create a test file
    test_file = "test_plaintext.txt"
    with open(test_file, 'w') as f:
        f.write("This is a secret message for testing encryption!\n")
        f.write("BLAKE2s + HMAC + AES = Secure encryption system")
    
    password = "my_secure_password_123"
    
    print("Testing CBC mode:")
    encryptor.encrypt_file_cbc(test_file, "test_encrypted_cbc.enc", password)
    print("✓ File encrypted (CBC)")
    
    success, msg = encryptor.decrypt_file("test_encrypted_cbc.enc", "test_decrypted_cbc.txt", password)
    print(f"✓ Decryption: {msg}")
    
    print("\nTesting CTR mode:")
    encryptor.encrypt_file_ctr(test_file, "test_encrypted_ctr.enc", password)
    print("✓ File encrypted (CTR)")
    
    success, msg = encryptor.decrypt_file("test_encrypted_ctr.enc", "test_decrypted_ctr.txt", password)
    print(f"✓ Decryption: {msg}")
    
    print("\nTesting wrong password:")
    success, msg = encryptor.decrypt_file("test_encrypted_cbc.enc", "test_fail.txt", "wrong_password")
    print(f"✗ Decryption with wrong password: {msg}")
