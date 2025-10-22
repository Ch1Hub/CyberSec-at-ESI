import numpy as np


def euclideEtendu(a, b):
    r, r1 = a, b
    u, u1 = 1, 0
    v, v1 = 0, 1
    while r1 != 0:
        q = r // r1
        r, r1, u, u1, v, v1 = r1, r - q*r1, u1, u - q*u1, v1, v - q*v1
    return r, u, v


def invMod(a, m):
    gcd, x, y = euclideEtendu(a, m)
    return x % m if gcd == 1 else -1



def hillEnc(plainText, key):
    n = key.shape[0]
    alphabet = [chr(i + ord('A')) for i in range(26)] + [" "]
    mapping = {c: i for i, c in enumerate(alphabet)}
    reverse_mapping = {i: c for c, i in mapping.items()}

 
    values = [mapping[c] for c in plainText]
    while len(values) % n != 0:
        values.append(mapping[" "])

    cypherText = ""
    for i in range(0, len(values), n):
        block = np.array(values[i:i+n])
        result = np.dot(key, block) % 27
        cypherText += ''.join(reverse_mapping[int(x)] for x in result)
    return cypherText

def hillDec(cypherText, key):
    n = key.shape[0]
    alphabet = [chr(i + ord('A')) for i in range(26)] + [" "]
    mapping = {c: i for i, c in enumerate(alphabet)}
    reverse_mapping = {i: c for c, i in mapping.items()}

 
    det = round(np.linalg.det(key)) % 27
    det_inv = invMod(int(det), 27)
    if det_inv == -1:
        return "Matrix not invertible modulo 27"

 
    key_inv = (det_inv * np.round(det * np.linalg.inv(key)).astype(int)) % 27

    values = [mapping[c] for c in cypherText]
    plainText = ""
    for i in range(0, len(values), n):
        block = np.array(values[i:i+n])
        result = np.dot(key_inv, block) % 27
        plainText += ''.join(reverse_mapping[int(x)] for x in result)
    return plainText


msg = "HELLO WORLD"
key = np.array([[3, 10, 20],
                [20, 9, 17],
                [9, 4, 17]])

encrypted = hillEnc(msg, key)
print("Encrypted:", encrypted)

decrypted = hillDec(encrypted, key)
print("Decrypted:", decrypted)

