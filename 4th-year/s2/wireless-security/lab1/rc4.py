def crc_msb_manual(data_str, poly_str):
    # Padding data with degree of polynomial (4 zeros)
    degree = len(poly_str) - 1
    padded_data = list(data_str + '0' * degree)
    poly = list(poly_str)
    
    print(f"--- CRC Step (MSB First) ---")
    print(f"Initial Padded Data: {''.join(padded_data)}")
    
    # Binary Division (XOR)
    for i in range(len(data_str)):
        if padded_data[i] == '1':
            print(f"Step {i}: XORing at position {i}")
            for j in range(len(poly)):
                # Perform XOR bit by bit
                padded_data[i + j] = str(int(padded_data[i + j]) ^ int(poly[j]))
            print(f"   Current State: {''.join(padded_data)}")
        else:
            print(f"Step {i}: Leading bit is 0, skipping...")
            
    remainder = ''.join(padded_data[-degree:])
    print(f"Final ICV (Remainder): {remainder}\n")
    return remainder

def rc4_ksa(key):
    print(f"--- RC4 KSA Step ---")
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    print(f"S-box initialized (first 10 elements): {S[:10]}...")
    return S

def rc4_prga(S, length):
    print(f"--- RC4 PRGA Step ---")
    i = 0
    j = 0
    keystream = []
    for _ in range(length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        keystream.append(K)
    print(f"Generated Keystream (bytes): {keystream}")
    return keystream

# --- Updated Execution Section ---
data = "10101010"
generator = "10011" # X^4 + X + 1 [cite: 13]
secret_key = [0x12, 0x34, 0x56, 0x78, 0x90] # 40-bit key [cite: 4, 15]
iv = [0xAA, 0xBB, 0xCC] # 24-bit IV [cite: 15, 20]

# 1. ICV Calculation [cite: 13]
icv = crc_msb_manual(data, generator)
full_payload = data + icv # [cite: 14]

# 2. RC4 Seed Formation [cite: 15, 17]
seed = iv + secret_key
s_box = rc4_ksa(seed)

# 3. Encryption (XOR) [cite: 10, 18, 20]
# We need enough keystream bytes to cover 12 bits (so 2 bytes)
keystream = rc4_prga(s_box, 2) 

print(f"--- Final Result ---")
print(f"Plaintext + ICV: {full_payload}")

# Correctly XORing bits by selecting the right byte from the keystream
ciphertext_bits = []
for i in range(len(full_payload)):
    byte_idx = i // 8
    bit_idx = 7 - (i % 8)
    bit_val = int(full_payload[i])
    key_bit = (keystream[byte_idx] >> bit_idx) & 1
    ciphertext_bits.append(str(bit_val ^ key_bit))

ciphertext = "".join(ciphertext_bits)
print(f"Ciphertext: {ciphertext}")
print(f"Transmitted Frame (IV + Ciphertext): {''.join(format(x, '08b') for x in iv)} + {ciphertext}") #