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
        return ValueError(f"inversed modular doesn't exist for {a} modulo {b}")
    else:
        return x % b


print(euclideEtendu(230597219691238, 12394872139561))

print(invMod(230597219691238,12394872139561))

print((11385906686156 * 230597219691238) % 12394872139561)
