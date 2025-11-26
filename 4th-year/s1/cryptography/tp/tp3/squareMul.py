def squareMultiply(x, c, n):

    c_binary = bin(c)[2:]
    
    z = 1
    
    for i in range(len(c_binary)):
        z = (z * z) % n
        
        if c_binary[i] == '1':
            z = (z * x) % n
    
    return z


def rsa_encrypt(m, e, n):
    return squareMultiply(m, e, n)


def rsa_decrypt(c, d, n):
    return squareMultiply(c, d, n)


def test_squareMultiply():
    
    result1 = squareMultiply(2, 512, 567)
    print(f"2^512 mod 567 = {result1}")

    result2 = squareMultiply(3453, 451235, 13)
    print(f"3453^451235 mod 13 = {result2}")

    result3 = squareMultiply(1024, 1024, 5678098)
    print(f"1024^1024 mod 5678098 = {result3}")


def test_rsa():
    
    p = 982451653
    q = 982451679
    n = p * q
    e = 128
    d = 512
    
    message = 123
    
    encrypted = rsa_encrypt(message, e, n)
    print(f"Encrypted: {encrypted}")
    
    decrypted = rsa_decrypt(encrypted, d, n)
    print(f"Decrypted: {decrypted}")


if __name__ == "__main__":
    test_squareMultiply()
    print()
    test_rsa()