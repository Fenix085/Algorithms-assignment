#task one: implementation of bubble sort, insertion sort, merge sort and quick sort
import random

def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
# ----------------------------------------------------------------
def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
# ----------------------------------------------------------------
def mergeSort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    lHalf = arr[:mid]
    rHalf = arr[mid:]

    sorted_l = mergeSort(lHalf)
    sorted_r = mergeSort(rHalf)

    return merge(sorted_l, sorted_r)

def merge(l, r):
    result = []
    i = j = 0
    while i < len(l) and j < len(r):
        if l[i] < r[j]:
            result.append(l[i])
            i += 1
        else:
            result.append(r[j])
            j += 1

    result.extend(l[i:])
    result.extend(r[j:])

    return result

# ----------------------------------------------------------------

def quickSort(arr, l = 0, r = None):
    if r is None:
        r = len(arr) - 1
    
    if l < r:
        pivot_index = random.randint(l, r)
        arr[pivot_index], arr[r] = arr[r], arr[pivot_index]
        pivot = arr[r]
        pivot = partition(arr, l, r)
        quickSort(arr, l, pivot - 1)
        quickSort(arr, pivot + 1, r)
    return arr

def partition(arr, l, r):
    pivot = arr[r]
    i = l - 1
    for j in range(l, r):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[r] = arr[r], arr[i + 1]
    return i + 1




if __name__ == "__main__":
    pass
    # arr = [64, 34, 25, 12, 22, 11, 90]

    # fin_arr = bubbleSort(arr.copy())
    # print("Sorted array:", fin_arr)
    # fin_arr = insertionSort(arr.copy())
    # print("Sorted array:", fin_arr)
    # fin_arr = mergeSort(arr.copy())
    # print("Sorted array:", fin_arr)
    # fin_arr = quickSort(arr.copy())
    # print("Sorted array:", fin_arr)