import numpy as np
import string

A = string.ascii_uppercase
idx = {c: i for i, c in enumerate(A)}
rev = {i: c for c, i in idx.items()}

def mod_inverse(a, m=26):
    for x in range(m):
        if (a * x) % m == 1:
            return x
    return None

def mat_mod_inv(M, mod=26):
    a, b = int(M[0, 0]), int(M[0, 1])
    c, d = int(M[1, 0]), int(M[1, 1])
    det = (a * d - b * c) % mod
    inv_det = mod_inverse(det, mod)
    if inv_det is None:
        raise ValueError("Matrix not invertible mod 26")
    adj = np.array([[d, -b], [-c, a]]) % mod
    return (inv_det * adj) % mod



M = np.array([[idx['B'], idx['N']],
              [idx['O'], idx['J']]])


C = np.array([[idx['V'], idx['G']],
              [idx['J'], idx['Z']]])


invM = mat_mod_inv(M)
A_key = (C.dot(invM)) % 26
invA = mat_mod_inv(A_key)


ciphertext = "VJGZMIKJZJ"  
plaintext = ""

for i in range(0, len(ciphertext), 2):
    block = ciphertext[i:i+2]
    vec = np.array([[idx[block[0]]], [idx[block[1]]]])
    pv = (invA.dot(vec) % 26).astype(int)
    plaintext += rev[int(pv[0, 0])] + rev[int(pv[1, 0])]

print("Key matrix A:\n", A_key)
print("Inverse key matrix A⁻¹ mod 26:\n", invA)
print("Decrypted message:", plaintext)

