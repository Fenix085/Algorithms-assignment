#task one: implementation of bubble sort, insertion sort, merge sort and quick sort
import random
import time

class Sorter:
    def __init__(self):
        pass


    # ---Bubble Sort-------------------------------------------------------------
    @staticmethod
    def bubbleSort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    # ---Insertion Sort-------------------------------------------------------------
    @staticmethod
    def insertionSort(arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    # ---Merge Sort-------------------------------------------------------------
    @staticmethod
    def mergeSort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        lHalf = arr[:mid]
        rHalf = arr[mid:]

        sorted_l = Sorter.mergeSort(lHalf)
        sorted_r = Sorter.mergeSort(rHalf)

        return Sorter.merge(sorted_l, sorted_r)

    @staticmethod
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

    # ---Quick Sort-------------------------------------------------------------

    @staticmethod
    def quickSort(arr, l = 0, r = None):
        if r is None:
            r = len(arr) - 1
        
        if l < r:
            pivot_index = random.randint(l, r)
            arr[pivot_index], arr[r] = arr[r], arr[pivot_index]
            pivot = Sorter.partition(arr, l, r)
            Sorter.quickSort(arr, l, pivot - 1)
            Sorter.quickSort(arr, pivot + 1, r)
        return arr

    @staticmethod
    def partition(arr, l, r):
        pivot = arr[r]
        i = l - 1
        for j in range(l, r):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[r] = arr[r], arr[i + 1]
        return i + 1
    
    #----Multi-Pivot Quick Sort-------------------------------------------------

    @staticmethod

    # ---Radix Sort-------------------------------------------------------------

    @staticmethod
    def radixSort(arr): #(or another, idk)
        if len(arr) == 0:
            return arr
        radixArray = [[], [], [], [], [], [], [], [], [], []]
        maxVal = max(arr)
        exp = 1

        while maxVal // exp > 0:

            while len(arr) > 0:
                val = arr.pop()
                radixIndex = (val // exp) % 10
                radixArray[radixIndex].append(val)

            for bucket in radixArray:
                while len(bucket) > 0:
                    val = bucket.pop()
                    arr.append(val)

            exp *= 10

        return arr
    
    # ---Heap Sort-------------------------------------------------------------
    
    @staticmethod
    def heapSort(arr):
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            Sorter.heapify(arr, n, i)

        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            Sorter.heapify(arr, i, 0)

        return arr

    @staticmethod
    def heapify(arr, n, i):
        largest = i
        l = 2*i + 1
        r = 2*i + 2

        if l < n and arr[l] > arr[largest]:
            largest = l

        if r < n and arr[r] > arr[largest]:
            largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            Sorter.heapify(arr, n, largest)   

    # ---Miracle Sort-------------------------------------------------------------

    @staticmethod
    def miracleSort(arr):
        while not Sorter.check(arr):
            time.sleep(1) # wait for a miracle
        return arr
    
    # ---Bogo Sort-------------------------------------------------------------

    @staticmethod
    def bogoSort(arr):
        while not Sorter.check(arr):
            random.shuffle(arr)
        return arr
    
    # ----------------------------------------------------------------

    @staticmethod
    def check(arr):
        # for i in range(1, len(arr)):
        #     if arr[i - 1] > arr[i]:
        #         return False
        # return True
        return False if any(arr[i - 1] > arr[i] for i in range(1, len(arr))) else True
    
    # ---Stalin Sort-------------------------------------------------------------

    @staticmethod
    def stalinSort(arr):
        if len(arr) == 0:
            return arr
        purged = [arr[0]]
        for i in range(1, len(arr)):
            if arr[i] >= purged[-1]:
                purged.append(arr[i])
        return purged

    # ---Communism Sort-------------------------------------------------------------
    
    @staticmethod
    def communizmSort(arr):
        if len(arr) == 0:
            return arr
        return [min(arr)] * len(arr)
    
if __name__ == "__main__":
    pass
    # arr = [1, 2, 3, 1, 3, 64, 128, 32, 0, 512, 256]
    # oSorter = Sorter()
    # arr = oSorter.stalinSort(arr)
    # print("Sorted array is:", arr)