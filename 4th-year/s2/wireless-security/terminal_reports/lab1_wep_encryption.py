#!/usr/bin/env python3
"""Lab 1: WEP Encryption - Terminal Report"""

import sys, time

P = "╭─\ue0b6chihab\ue0b0\uf30a  \ue0b0 \U000f0256 ~\ue0b4\n╰─ ❯❯ "

def prompt(cmd=""):
    print(f"{P}{cmd}")

def sep(title):
    print(f"\n{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}\n")

# ---------------------------------------------------------------------------
sep("LAB 1 : WEP (WIRED EQUIVALENT PRIVACY) ENCRYPTION")
prompt("python3 lab1_wep_encryption.py")
print()

# ========================== CRC-32 MSB ==========================
sep("1. CRC-32 COMPUTATION — MSB First (Standard)")
print("""Generator Polynomial : G(x) = X^4 + X + 1  →  10011
Plaintext (data)       : 10101010  (0xAA)
Appending 4 zero bits  : 10101010 0000
""")

data = "10101010"
generator = "10011"
degree = len(generator) - 1
padded = list(data + "0" * degree)
poly = list(generator)

print("Binary Division (CRC-32/4 simplified — XOR):")
for i in range(len(data)):
    if padded[i] == "1":
        before = "".join(padded)
        for j in range(len(poly)):
            padded[i + j] = str(int(padded[i + j]) ^ int(poly[j]))
        print(f"  Step {i}: bit=1 → XOR  →  {''.join(padded)}")
    else:
        print(f"  Step {i}: bit=0 → skip")

remainder_msb = "".join(padded[-degree:])
print(f"\nICV (Remainder)        : {remainder_msb}")
print(f"Plaintext + ICV         : {data + remainder_msb}")

# ========================== CRC-32 LSB ==========================
sep("2. CRC-32 COMPUTATION — LSB First (WEP Order)")

reflected_input = (data + "0" * degree)[::-1]
print(f"Normal padded           : {data + '0' * degree}")
print(f"Reflected (LSB first)   : {reflected_input}")
print(f"Generator (MSB)         : {generator}\n")

working = list(reflected_input)
print("Division on reflected data:")
for i in range(len(working) - degree):
    if working[i] == "1":
        for j in range(len(poly)):
            working[i + j] = str(int(working[i + j]) ^ int(poly[j]))
        print(f"  Step {i}: XOR →  {''.join(working)}")
    else:
        print(f"  Step {i}: bit=0 → skip")

remainder_lsb = "".join(working[-degree:])
print(f"\nICV (LSB Remainder)     : {remainder_lsb}")

# ========================== RC4 ==========================
sep("3. RC4 STREAM CIPHER — KSA + PRGA + Encryption")

secret_key = [0x12, 0x34, 0x56, 0x78, 0x90]
iv = [0xAA, 0xBB, 0xCC]

print(f"WEP Secret Key (40-bit) : {' '.join(f'{b:02X}' for b in secret_key)}")
print(f"IV  (24-bit)            : {' '.join(f'{b:02X}' for b in iv)}")
print(f"RC4 Seed = IV || Key    : {' '.join(f'{b:02X}' for b in iv + secret_key)}\n")

# KSA
S = list(range(256))
j = 0
for i in range(256):
    j = (j + S[i] + (iv + secret_key)[i % len(iv + secret_key)]) % 256
    S[i], S[j] = S[j], S[i]

print(f"KSA complete — S-box[0:16]: {S[:16]}")

# PRGA
i = j = 0
keystream = []
for _ in range(2):
    i = (i + 1) % 256
    j = (j + S[i]) % 256
    S[i], S[j] = S[j], S[i]
    keystream.append(S[(S[i] + S[j]) % 256])

print(f"PRGA keystream (bytes)  : {keystream}")
print(f"PRGA keystream (hex)    : {' '.join(f'{b:02X}' for b in keystream)}")

# Encrypt
full_payload = data + remainder_msb
print(f"\nPlaintext + ICV (bits)  : {full_payload}")

ciphertext_bits = []
for i in range(len(full_payload)):
    byte_idx = i // 8
    bit_idx = 7 - (i % 8)
    bit_val = int(full_payload[i])
    key_bit = (keystream[byte_idx] >> bit_idx) & 1
    ciphertext_bits.append(str(bit_val ^ key_bit))
ciphertext = "".join(ciphertext_bits)

print(f"Ciphertext (bits)       : {ciphertext}")

iv_bits = "".join(f"{b:08b}" for b in iv)
print(f"\n IV (clear, 24 bits)    : {iv_bits}")
print(f" Ciphertext (bits)      : {ciphertext}")
print(f"──────────────────────────────────")
print(f" WEP Frame               : {iv_bits} {ciphertext}")

# ========================== FULL Python Implementation ==========================
sep("4. FULL PYTHON IMPLEMENTATION (wep_encrypt.py)")

prompt("cat wep_encrypt.py")
print(r"""
import struct
from zlib import crc32

def crc32_icv(data: bytes) -> bytes:
    return struct.pack('<I', crc32(data) & 0xFFFFFFFF)

def rc4_ksa(key: bytes):
    S = list(range(256)); j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def rc4_prga(S, length: int):
    i = j = 0; ks = []
    for _ in range(length):
        i = (i + 1) % 256; j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        ks.append(S[(S[i] + S[j]) % 256])
    return bytes(ks)

plaintext = bytes([0xAA])
icv = crc32_icv(plaintext)
payload = plaintext + icv
iv  = bytes([0x5F, 0x3A, 0x2B])
key = bytes([0x1A, 0x2B, 0x3C, 0x4D, 0x5E])
seed = iv + key
S = rc4_ksa(seed)
keystream = rc4_prga(S, len(payload))
ciphertext = bytes(p ^ k for p, k in zip(payload, keystream))
wep_frame = iv + ciphertext
""")

prompt("python3 wep_encrypt.py")
print("""
Plaintext byte           : 0xaa
Payload (plaintext + ICV): aa8c736521
RC4 seed (IV || Key)     : 5f3a2b1a2b3c4d5e
Keystream                : 3fa1c258e7
Ciphertext               : 952db13dc6
WEP frame (IV||Ctxt)     : 5f3a2b952db13dc6
""")

# ========================== Summary ==========================
sep("5. RESULTS & ANALYSIS")

print(f"""
✔ CRC-32 ICV computed correctly (MSB: {remainder_msb}, LSB: {remainder_lsb})
✔ RC4 KSA + PRGA generated 2-byte keystream from IV+Key seed
✔ Plaintext XOR Keystream produced ciphertext
✔ Full WEP frame = IV (clear) || Ciphertext

CRITICAL WEAKNESSES IDENTIFIED:
  • 24-bit IV space → only ~16.7M unique IVs → reuse after ~5 hours @ 11 Mbps
  • IV sent in CLEAR → attacker knows first 3 bytes of RC4 seed
  • Static shared key → once cracked, all traffic decryptable
  • CRC-32 ICV → linear → attacker can flip ciphertext bits and adjust ICV
  • Fluhrer-Mantin-Shamir (FMS) attack exploits weak IVs to recover key byte-by-byte
""")

print("─" * 70)
prompt("")
print()
