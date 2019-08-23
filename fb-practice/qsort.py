def qsort(arr):
    def recurse(lo, hi):
        if lo >= hi:
            return
        pivot = arr[(lo + hi) // 2]
        i = lo
        j = hi
        while True:
            while arr[i] < pivot:
                i += 1
            while arr[j] > pivot:
                j -= 1
            if i > j:
                break
            tmp = arr[i]
            arr[i] = arr[j]
            arr[j] = tmp
            i += 1
            j -= 1
        recurse(lo, j)
        recurse(i, hi)

    recurse(0, len(arr) - 1)
