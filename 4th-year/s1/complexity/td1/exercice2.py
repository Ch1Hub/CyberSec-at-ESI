def memoFib(n, tab):
    if tab[n]:
        return tab[n]
    elif n==1 or n ==0 :
        tab[n] = n
    else:
        tab[n] = memoFib(n-1, tab) + memoFib(n-2, tab)
    return tab[n]

def tabFib(n):
    tab = [None] * (n+1)
    tab[0] = 0
    tab[1] = 1
    for i in range(2,n+1):
        tab[i]= tab[i-1]+tab[i-2]
    return tab[n]

n= 20578
a= [None] * (n+1)
print(tabFib(n))


