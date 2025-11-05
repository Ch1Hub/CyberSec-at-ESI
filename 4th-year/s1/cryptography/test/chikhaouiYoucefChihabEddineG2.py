def ShamirShare(s, k, n, p=257):
    coeffs = [7, 1, 9]

    shares = []
    for x in range(1, n + 1):
        y = (coeffs[0] + coeffs[1]*x + coeffs[2]*(x**2)) % p
        shares.append((x, y))
    return shares


def ShamirReconstruct(shares, p=257):
    S = 0
    k = len(shares)

    for i in range(k):
        xi, yi = shares[i]
        li = 1
        for j in range(k):
            if i != j:
                xj, _ = shares[j]
                li *= (-xj) * pow(xi - xj, -1, p)
                li %= p
        S = (S + yi * li) % p
    return S
p = 257
s = 7
k = 3
n = 5
shares = ShamirShare(s, k, n, p)
print("Parts distribuees :", shares)
subset = [shares[0], shares[1], shares[2]]
S_reconstructed = ShamirReconstruct(subset, p)
print("Secret reconstruit par le president et un membre:", S_reconstructed)
subset = [shares[2], shares[3], shares[4]]
S_reconstructed = ShamirReconstruct(subset, p)
print("Secret reconstruit par les 3 membres:", S_reconstructed)
subset = [shares[2], shares[3]]
S_reconstructed = ShamirReconstruct(subset, p)
print("Secret eronnee reconstruit par juste 2 membre:", S_reconstructed)
