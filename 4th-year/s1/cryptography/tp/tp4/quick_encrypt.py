#!/usr/bin/env python3
"""
Quick command-line file encryption/decryption tool
Usage:
    python quick_encrypt.py encrypt <input_file> <output_file> <password> [mode]
    python quick_encrypt.py decrypt <input_file> <output_file> <password>
"""

import sys
from file_encryption import AuthenticatedFileEncryption


def print_usage():
    print("Authenticated File Encryption Tool")
    print()
    print("Usage:")
    print("  Encrypt: python quick_encrypt.py encrypt <input> <output> <password> [CBC|CTR]")
    print("  Decrypt: python quick_encrypt.py decrypt <input> <output> <password>")
    print()
    print("Examples:")
    print("  python quick_encrypt.py encrypt secret.txt secret.enc MyPass123 CBC")
    print("  python quick_encrypt.py decrypt secret.enc decrypted.txt MyPass123")


def main():
    if len(sys.argv) < 5:
        print_usage()
        sys.exit(1)
    
    operation = sys.argv[1].lower()
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    password = sys.argv[4]
    
    encryptor = AuthenticatedFileEncryption()
    
    try:
        if operation == 'encrypt':
            mode = sys.argv[5].upper() if len(sys.argv) > 5 else 'CBC'
            if mode not in ['CBC', 'CTR']:
                print(f"Error: Invalid mode '{mode}'. Use CBC or CTR.")
                sys.exit(1)
            
            print(f"Encrypting {input_file} -> {output_file}")
            print(f"Mode: {mode}")
            
            metadata = encryptor.encrypt_file(input_file, output_file, password, mode)
            
            print(f"✓ Success!")
            print(f"  Original: {metadata['input_size']} bytes")
            print(f"  Encrypted: {metadata['output_size']} bytes")
            print(f"  Tag: {metadata['tag'][:32]}...")
            
        elif operation == 'decrypt':
            print(f"Decrypting {input_file} -> {output_file}")
            
            metadata = encryptor.decrypt_file(input_file, output_file, password)
            
            print(f"✓ Success!")
            print(f"  Mode: {metadata['mode']}")
            print(f"  Size: {metadata['output_size']} bytes")
            print(f"  Authenticated: YES")
            
        else:
            print(f"Error: Unknown operation '{operation}'")
            print_usage()
            sys.exit(1)
            
    except FileNotFoundError as e:
        print(f"✗ Error: File not found - {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
