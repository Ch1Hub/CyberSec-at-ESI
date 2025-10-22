def euclideEtendu(a,b):
    r = a
    r1 = b
    u = 1
    v = 0
    u1 = 0
    v1 = 1
    while r1 != 0:
        q = r // r1
        rs = r
        us = u
        vs = v
        r = r1
        u = u1
        v = v1
        r1= rs - q*r1
        u1= us - q*u1
        v1 = vs - q*v1
    return r, u, v

def invMod(a,b):
    gcd, x, y = euclideEtendu(a, b)
    if gcd != 1:
        return -1
    else:
        return x % b

def affineEnc(plainText, key):
    cypherText = ""
    for char in plainText:
        value = 26 if char == " " else ord(char) - ord("A")
        cypherIndex = (key[0] * value + key[1]) % 27
        cypherText += " " if cypherIndex == 26 else chr(cypherIndex + ord("A"))
    return cypherText

def affineDec(cypherText, key):
    plainText = ""
    keyInverse = invMod(key[0], 27)
    if keyInverse == -1:
        return "The chosen key is not valid"
    for char in cypherText:
        value = 26 if char == " " else ord(char) - ord("A")
        plainIndex = (keyInverse * (value - key[1])) % 27
        plainText += " " if plainIndex == 26 else chr(plainIndex + ord("A"))
    return plainText

msg = "ABCDEFGHIJKLMNOPQRSTUVWXY Z"
key = [14, 10]
encrypted = affineEnc(msg, key)

print("the Affine Encrypted text of: '", msg, "' with the keys (",key[0],",",key[1],") is: ", encrypted)

decrypted = affineDec(encrypted, key)
print("the Affine Decrypted text of: '", msg, "' with the keys (",key[0],",",key[1],") is: ", decrypted)

