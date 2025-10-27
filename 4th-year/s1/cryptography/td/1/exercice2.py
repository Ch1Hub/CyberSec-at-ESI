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

def mulCesarEncryption(plainText, keyChar):
    cypherText= ""
    key = ord(keyChar) - ord("A")
    for i in range(0, len(plainText)):
        value = ord(plainText[i]) - ord("A")
        cypherIndex = (value * key) % 26 + ord("A")
        cypherText += chr(cypherIndex)
    return cypherText

def mulCesarDecryption(cypherText, keyChar):
    plainText = ""
    key = ord(keyChar) - ord("A")
    errorMessage = "The chosen key is not valid"
    if invMod(key, 26) == -1:
        return errorMessage
    else:
        keyInverse = invMod(key, 26)
        for i in range(0, len(cypherText)):
            value = ord(cypherText[i]) - ord("A")
            plainIndex = (value * keyInverse) % 26 + ord("A")
            plainText += chr(plainIndex)
        return plainText

print("The encryption of 'SECURITE' with 'P' as key is: ",mulCesarEncryption("SECURITE", "P"))

print("The decryption of 'XJQXZ' with 'B' as key is: ", mulCesarDecryption("XJQXZ", "B"))

print("The decryption of 'XJQXZ' with 'E' as key is: ", mulCesarDecryption("XJQXZ", "E"))

print("The decryption of 'XJQXZ' with 'M' as key is: ", mulCesarDecryption("XJQXZ", "M"))

print("The decryption of 'XJQXZ' with 'R' as key is: ", mulCesarDecryption("XJQXZ", "R"))





