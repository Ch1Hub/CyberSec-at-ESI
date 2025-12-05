"""
Authenticated File Encryption System
Uses AES encryption with BLAKE2s-based key derivation and HMAC authentication
"""

import os
import struct
from blake2s import blake2s
from hmac_blake2s import hmac_blake2s
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class AuthenticatedFileEncryption:
    """
    Authenticated encryption system for files.
    
    Features:
    - AES encryption in CBC or CTR mode
    - BLAKE2s-based key derivation from password
    - HMAC-BLAKE2s authentication
    - IV/Nonce stored with encrypted file
    """
    
    SALT_SIZE = 16  # 128 bits
    KEY_SIZE = 32   # 256 bits for AES-256
    IV_SIZE = 16    # 128 bits for AES
    TAG_SIZE = 32   # 256 bits for HMAC
    
    MODE_CBC = b'CBC'
    MODE_CTR = b'CTR'
    
    def __init__(self):
        """Initialize the encryption system"""
        pass
    
    def derive_key(self, password, salt):
        """
        Derive encryption key from password using BLAKE2s.
        
        Args:
            password: User password (string or bytes)
            salt: Random salt (bytes)
        
        Returns:
            tuple: (encryption_key, hmac_key) - both 32 bytes
        """
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        # Derive master key using BLAKE2s(password || salt)
        master_key = blake2s(password + salt, digest_size=32)
        
        # Derive encryption key: BLAKE2s(master_key || "encryption")
        encryption_key = blake2s(master_key + b"encryption", digest_size=32)
        
        # Derive HMAC key: BLAKE2s(master_key || "authentication")
        hmac_key = blake2s(master_key + b"authentication", digest_size=32)
        
        return encryption_key, hmac_key
    
    def encrypt_file(self, input_file, output_file, password, mode='CBC'):
        """
        Encrypt a file with authentication.
        
        Args:
            input_file: Path to file to encrypt
            output_file: Path for encrypted output
            password: Encryption password
            mode: Encryption mode ('CBC' or 'CTR')
        
        Returns:
            dict: Encryption metadata
        """
        # Validate mode
        if mode.upper() not in ['CBC', 'CTR']:
            raise ValueError("Mode must be 'CBC' or 'CTR'")
        
        mode = mode.upper()
        mode_bytes = self.MODE_CBC if mode == 'CBC' else self.MODE_CTR
        
        # Generate random salt and IV/nonce
        salt = get_random_bytes(self.SALT_SIZE)
        iv = get_random_bytes(self.IV_SIZE)
        
        # Derive keys
        encryption_key, hmac_key = self.derive_key(password, salt)
        
        # Read input file
        with open(input_file, 'rb') as f:
            plaintext = f.read()
        
        # Encrypt based on mode
        if mode == 'CBC':
            cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
            # Add PKCS7 padding
            padding_length = AES.block_size - (len(plaintext) % AES.block_size)
            plaintext += bytes([padding_length] * padding_length)
            ciphertext = cipher.encrypt(plaintext)
        else:  # CTR
            # CTR mode uses a counter constructed from the IV
            from Crypto.Util import Counter
            ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
            cipher = AES.new(encryption_key, AES.MODE_CTR, counter=ctr)
            ciphertext = cipher.encrypt(plaintext)
        
        # Compute HMAC over: mode || salt || iv || ciphertext
        data_to_authenticate = mode_bytes + salt + iv + ciphertext
        tag = hmac_blake2s(hmac_key, data_to_authenticate, digest_size=self.TAG_SIZE)
        
        # Build output: [mode(3)] [salt(16)] [iv(16)] [ciphertext(variable)] [tag(32)]
        encrypted_data = mode_bytes + salt + iv + ciphertext + tag
        
        # Write encrypted file
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)
        
        metadata = {
            'mode': mode,
            'salt': salt.hex(),
            'iv': iv.hex(),
            'input_size': len(plaintext) - (padding_length if mode == 'CBC' else 0),
            'output_size': len(encrypted_data),
            'tag': tag.hex()
        }
        
        return metadata
    
    def decrypt_file(self, input_file, output_file, password):
        """
        Decrypt and verify an authenticated encrypted file.
        
        Args:
            input_file: Path to encrypted file
            output_file: Path for decrypted output
            password: Decryption password
        
        Returns:
            dict: Decryption metadata
        
        Raises:
            ValueError: If authentication fails or file is corrupted
        """
        # Read encrypted file
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()
        
        # Minimum size check
        min_size = 3 + self.SALT_SIZE + self.IV_SIZE + self.TAG_SIZE
        if len(encrypted_data) < min_size:
            raise ValueError("Invalid encrypted file: too small")
        
        # Parse header
        mode_bytes = encrypted_data[:3]
        salt = encrypted_data[3:3 + self.SALT_SIZE]
        iv = encrypted_data[3 + self.SALT_SIZE:3 + self.SALT_SIZE + self.IV_SIZE]
        ciphertext = encrypted_data[3 + self.SALT_SIZE + self.IV_SIZE:-self.TAG_SIZE]
        tag = encrypted_data[-self.TAG_SIZE:]
        
        # Validate mode
        if mode_bytes == self.MODE_CBC:
            mode = 'CBC'
        elif mode_bytes == self.MODE_CTR:
            mode = 'CTR'
        else:
            raise ValueError(f"Unknown encryption mode: {mode_bytes}")
        
        # Derive keys
        encryption_key, hmac_key = self.derive_key(password, salt)
        
        # Verify HMAC
        data_to_authenticate = mode_bytes + salt + iv + ciphertext
        expected_tag = hmac_blake2s(hmac_key, data_to_authenticate, digest_size=self.TAG_SIZE)
        
        # Constant-time comparison
        if not self._constant_time_compare(tag, expected_tag):
            raise ValueError("Authentication failed: Invalid password or corrupted file")
        
        # Decrypt based on mode
        if mode == 'CBC':
            cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
            plaintext = cipher.decrypt(ciphertext)
            # Remove PKCS7 padding
            padding_length = plaintext[-1]
            if not (1 <= padding_length <= AES.block_size):
                raise ValueError("Invalid padding")
            plaintext = plaintext[:-padding_length]
        else:  # CTR
            # CTR mode uses a counter constructed from the IV
            from Crypto.Util import Counter
            ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
            cipher = AES.new(encryption_key, AES.MODE_CTR, counter=ctr)
            plaintext = cipher.decrypt(ciphertext)
        
        # Write decrypted file
        with open(output_file, 'wb') as f:
            f.write(plaintext)
        
        metadata = {
            'mode': mode,
            'salt': salt.hex(),
            'iv': iv.hex(),
            'output_size': len(plaintext),
            'verified': True
        }
        
        return metadata
    
    @staticmethod
    def _constant_time_compare(a, b):
        """Constant-time comparison to prevent timing attacks"""
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0


def main():
    """Interactive CLI for file encryption/decryption"""
    import sys
    
    encryptor = AuthenticatedFileEncryption()
    
    print("=" * 70)
    print("Authenticated File Encryption System")
    print("Using AES + BLAKE2s + HMAC-BLAKE2s")
    print("=" * 70)
    
    while True:
        print("\nOptions:")
        print("1. Encrypt file")
        print("2. Decrypt file")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            # Encryption
            print("\n--- FILE ENCRYPTION ---")
            input_file = input("Input file path: ").strip()
            
            if not os.path.exists(input_file):
                print(f"Error: File '{input_file}' not found!")
                continue
            
            output_file = input("Output file path: ").strip()
            
            print("\nEncryption modes:")
            print("1. CBC (Cipher Block Chaining)")
            print("2. CTR (Counter Mode)")
            mode_choice = input("Select mode (1-2): ").strip()
            
            mode = 'CBC' if mode_choice == '1' else 'CTR'
            
            password = input("Enter password: ").strip()
            if len(password) < 8:
                print("Warning: Password should be at least 8 characters!")
                confirm = input("Continue anyway? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue
            
            try:
                print("\nEncrypting...")
                metadata = encryptor.encrypt_file(input_file, output_file, password, mode)
                
                print("\n✓ Encryption successful!")
                print(f"  Mode: {metadata['mode']}")
                print(f"  Original size: {metadata['input_size']} bytes")
                print(f"  Encrypted size: {metadata['output_size']} bytes")
                print(f"  Salt: {metadata['salt'][:32]}...")
                print(f"  IV: {metadata['iv'][:32]}...")
                print(f"  HMAC Tag: {metadata['tag'][:32]}...")
                print(f"\nEncrypted file saved to: {output_file}")
                
            except Exception as e:
                print(f"\n✗ Encryption failed: {e}")
        
        elif choice == '2':
            # Decryption
            print("\n--- FILE DECRYPTION ---")
            input_file = input("Encrypted file path: ").strip()
            
            if not os.path.exists(input_file):
                print(f"Error: File '{input_file}' not found!")
                continue
            
            output_file = input("Output file path: ").strip()
            password = input("Enter password: ").strip()
            
            try:
                print("\nDecrypting and verifying...")
                metadata = encryptor.decrypt_file(input_file, output_file, password)
                
                print("\n✓ Decryption and verification successful!")
                print(f"  Mode: {metadata['mode']}")
                print(f"  Decrypted size: {metadata['output_size']} bytes")
                print(f"  Authentication: VERIFIED")
                print(f"\nDecrypted file saved to: {output_file}")
                
            except ValueError as e:
                print(f"\n✗ Decryption failed: {e}")
            except Exception as e:
                print(f"\n✗ Error: {e}")
        
        elif choice == '3':
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
