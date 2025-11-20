import time
import random
from statistics import mean
import sorter
import csv
import matplotlib.pyplot as plt

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

if __name__ == "__main__":

    choice = input("1 - run tests (task1A), 2 - Olsen Gang (task1B): ")

    oSorter = sorter.Sorter()

    match choice.strip():
        case '1':
            sizes = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]
            sizes_long = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]

            version = input("1 for quick (default), 2 for long (really long, I did maximum for 10000, it will have to sort array of 50000 elements 30 times): ")
            if version.strip() == '2':
                sizes = sizes_long

            results = { 'bubble': [], 'insertion': [], 'merge': [], 'quick': [] }

            for n in sizes:
                for name, func in [('bubble', oSorter.bubbleSort),
                                ('insertion', oSorter.insertionSort),
                                ('merge', oSorter.mergeSort),
                                ('quick', oSorter.quickSort)]:
                    avg = measure(func, n)
                    results[name].append(avg)
                    print(f"{name} n={n}: {avg:.6f} s")
           
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
        case '2':
            with open("carddump2.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    exp_date = row['Expiry Date']
                    pin = row['PIN']
            # print(rows[0])