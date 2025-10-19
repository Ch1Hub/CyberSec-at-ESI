def insertionSort(tab):
    for i in range(1, len(tab)):
        pivot= tab[i]
        j = i-1
        while j >= 0 and pivot < tab[j]:
            tab[j+1] = tab[j] 
            j-=1
        tab[j+1] = pivot
    return tab

a = [9,8,7,6,5,4,3,2,1] 

print(insertionSort(a))
