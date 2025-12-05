# Authenticated File Encryption System

## Overview

A secure file encryption system using:
- **AES-256** encryption (CBC or CTR mode)
- **BLAKE2s** for key derivation from password
- **HMAC-BLAKE2s** for authentication

## Features

✓ Password-based encryption  
✓ Two encryption modes: CBC and CTR  
✓ Authenticated encryption (prevents tampering)  
✓ Random salt and IV for each encryption  
✓ Secure key derivation  

## Files

- `blake2s.py` - BLAKE2s hash function implementation
- `hmac_blake2s.py` - HMAC-BLAKE2s authentication
- `file_encryption.py` - Main encryption application
- `test_encryption.py` - Automated tests

## Usage

### Interactive Mode

Run the application:
```bash
python file_encryption.py
```

Follow the prompts to:
1. Select encrypt or decrypt
2. Choose input/output files
3. Select encryption mode (CBC or CTR)
4. Enter password

### Programmatic Usage

```python
from file_encryption import AuthenticatedFileEncryption

encryptor = AuthenticatedFileEncryption()

# Encrypt a file
metadata = encryptor.encrypt_file(
    input_file='secret.txt',
    output_file='secret.enc',
    password='MyPassword123',
    mode='CBC'  # or 'CTR'
)

# Decrypt a file
metadata = encryptor.decrypt_file(
    input_file='secret.enc',
    output_file='secret_decrypted.txt',
    password='MyPassword123'
)
```

## File Format

Encrypted files have the following structure:

```
[Mode (3 bytes)] [Salt (16 bytes)] [IV (16 bytes)] [Ciphertext] [HMAC Tag (32 bytes)]
```

- **Mode**: "CBC" or "CTR" (identifies encryption mode)
- **Salt**: Random 128-bit salt for key derivation
- **IV**: Random 128-bit initialization vector
- **Ciphertext**: Encrypted data
- **HMAC Tag**: 256-bit authentication tag

## Security Features

### Key Derivation
```
master_key = BLAKE2s(password || salt)
encryption_key = BLAKE2s(master_key || "encryption")
hmac_key = BLAKE2s(master_key || "authentication")
```

### Authentication
HMAC computed over: `mode || salt || iv || ciphertext`

### Protection Against
- ✓ Password guessing (with strong passwords)
- ✓ Tampering detection
- ✓ Ciphertext modification
- ✓ Mode confusion
- ✓ Replay attacks (unique salt/IV per encryption)

## Encryption Modes

### CBC (Cipher Block Chaining)
- Traditional block cipher mode
- Requires padding (PKCS7)
- Sequential encryption
- Good for general purpose

### CTR (Counter Mode)
- Stream cipher mode
- No padding required
- Can be parallelized
- Slightly smaller output

## Testing

Run automated tests:
```bash
python test_encryption.py
```

Tests include:
- CBC mode encryption/decryption
- CTR mode encryption/decryption
- Wrong password rejection
- Tampered file detection

## Example Session

```
$ python file_encryption.py

======================================================================
Authenticated File Encryption System
Using AES + BLAKE2s + HMAC-BLAKE2s
======================================================================

Options:
1. Encrypt file
2. Decrypt file
3. Exit

Select option (1-3): 1

--- FILE ENCRYPTION ---
Input file path: document.pdf
Output file path: document.pdf.enc

Encryption modes:
1. CBC (Cipher Block Chaining)
2. CTR (Counter Mode)
Select mode (1-2): 1
Enter password: ********

Encrypting...

✓ Encryption successful!
  Mode: CBC
  Original size: 12543 bytes
  Encrypted size: 12624 bytes
  Salt: a3f2c8d1e9b4f7c2...
  IV: 7d8e2f9a4b6c1e3d...
  HMAC Tag: 9f3e7a2c8d1b4e6f...

Encrypted file saved to: document.pdf.enc
```

## Security Notes

⚠️ **Password Strength**: Use strong passwords (at least 12 characters with mixed case, numbers, symbols)

⚠️ **Password Storage**: Never store passwords in plain text

⚠️ **Key Management**: The security relies entirely on the password

⚠️ **Production Use**: This is educational code. For production, consider:
- Using established libraries (e.g., `cryptography` package)
- Hardware security modules (HSM)
- Key management systems
- Additional security audits

## How It Works

### Encryption Process

1. User provides password and file
2. Generate random salt (128 bits)
3. Derive encryption key and HMAC key from password + salt
4. Generate random IV (128 bits)
5. Encrypt file with AES-256 (CBC or CTR mode)
6. Compute HMAC over mode + salt + IV + ciphertext
7. Save: mode + salt + IV + ciphertext + tag

### Decryption Process

1. Read encrypted file
2. Extract mode, salt, IV, ciphertext, tag
3. Derive keys from password + salt
4. Verify HMAC tag (authenticate-then-decrypt)
5. If verification fails, reject immediately
6. Decrypt ciphertext with AES-256
7. Save decrypted file

## Requirements

```bash
pip install pycryptodome
```

The implementation uses:
- Custom BLAKE2s implementation (no external dependencies)
- Custom HMAC-BLAKE2s implementation
- PyCryptodome for AES encryption only

## License

Educational use only.
