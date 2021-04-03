def func(n,arr):
    maxAnoy = 0
    for i in range(n):
        anoy = 0
        for j in range(i):
            if(arr[i] < arr[j]):
                anoy += i - j
                print(i, j, anoy)

        if(anoy > maxAnoy):
            maxAnoy = anoy

    return maxAnoy

n = int(input())
arr = list(map(int, input().split()))
print(func(n, arr))