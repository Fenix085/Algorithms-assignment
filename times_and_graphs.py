import time
import random
from statistics import mean
import main_task_1
import csv

def random_array(n):
    return [random.randint(-5000, 5000) for _ in range(n)]

def measure(algo, n, reps=30):
    times = []
    for _ in range(reps):
        arr = random_array(n)
        arr_copy = arr[:]
        start = time.perf_counter()
        algo(arr_copy)
        end = time.perf_counter()
        times.append(end - start)
    return mean(times)

sizes = [5, 10, 20, 50, 100, 200, 500, 1000, 2000]
sizes_long = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]

version = input("1 for quick (default), 2 for long (really long, I did maximum for 10000): ")
if version.strip() == '2':
    sizes = sizes_long

results = { 'bubble': [], 'insertion': [], 'merge': [], 'quick': [] }

for n in sizes:
    for name, func in [('bubble', main_task_1.bubbleSort),
                       ('insertion', main_task_1.insertionSort),
                       ('merge', main_task_1.mergeSort),
                       ('quick', main_task_1.quickSort)]:
        avg = measure(func, n)
        results[name].append(avg)
        print(f"{name} n={n}: {avg:.6f} s")

import matplotlib.pyplot as plt

plt.figure()

plt.plot(sizes, results['bubble'], marker='o', label='Bubble sort')
plt.plot(sizes, results['insertion'], marker='o', label='Insertion sort')
plt.plot(sizes, results['merge'], marker='o', label='Merge sort')
plt.plot(sizes, results['quick'], marker='o', label='Quick sort')

plt.xlabel('Array size n')
plt.ylabel('Average running time (seconds)')
plt.title('Running time of sorting algorithms')
plt.legend()
plt.grid(True)

plt.show()


with open("sorting_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    # header
    writer.writerow(["n", "bubble", "insertion", "merge", "quick"])
    
    # one row per n
    for i, n in enumerate(sizes):
        writer.writerow([
            n,
            results["bubble"][i],
            results["insertion"][i],
            results["merge"][i],
            results["quick"][i],
        ])
