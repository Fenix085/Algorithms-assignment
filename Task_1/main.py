import sorter
import vector
import time
import random
from statistics import mean
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

def create_key(row):
    mm, yyyy = row["Expiry Date"].split('/')
    year = int(yyyy)
    month = int(mm)
    pin = int(row["PIN"])
    return year * 1000000 + month * 10000 + pin

def half_mixer(card_f: str, card_s: str) -> str:
    """
    card_f: 'nnnn-nnnn-nnnn-****' (dump1)
    card_s: '****-****-****-nnnn' (dump2)
    return: 'nnnn-nnnn-nnnn-nnnn'
    """
    parts_f = card_f.split("-")
    parts_s = card_s.split("-")

    # first 3 groups from first file, last group from second file
    return "-".join(parts_f[:3] + parts_s[3:])

if __name__ == "__main__":

    choice = input("1 - run tests (task1A), 2 - Olsen Gang (task1B): ")

    oSorter = sorter.Sorter()

    match choice.strip():
        case '1':
            sizes = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]
            sizes_long = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]

            version = input("1 - for quick (default), 2 - for long (really long, I did maximum for 10000, it will have to sort array of 50000 elements 30 times),\n" \
            "3 - for vector implementation: ")
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
            rows = []
            with open("carddump2.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)
            
            key_row_dict = { create_key(row): row for row in rows }
            sorted_keys = oSorter.radixSort(list(key_row_dict.keys()))
            rows = [key_row_dict[k] for k in sorted_keys]

            with open("carddump2_sorted.csv", "w", newline="") as f:
                filednames = rows[0].keys()
                writer = csv.DictWriter(f, fieldnames=filednames)
                writer.writeheader()
                writer.writerows(rows)

            # 1. Read dump1 (masked last 4)
            with open("carddump1.csv", "r", newline="") as f1:
                reader1 = csv.DictReader(f1)
                rows1 = list(reader1)

            # 2. Read sorted dump2 (masked first 12, real last 4)
            with open("carddump2_sorted.csv", "r", newline="") as f2:
                reader2 = csv.DictReader(f2)
                rows2 = list(reader2)

            # sanity check
            if len(rows1) != len(rows2):
                raise ValueError(f"Row count mismatch: dump1={len(rows1)}, dump2={len(rows2)}")

            # 3. Build final rows
            output_rows = []
            for row1, row2 in zip(rows1, rows2):
                card_f = row1["Credit Card Number"]
                card_s = row2["Credit Card Number"]

                full_card = half_mixer(card_f, card_s)

                # Take all other fields from dump2 row (has expiry, PIN, CVV, etc.)
                new_row = row2.copy()
                new_row["Credit Card Number"] = full_card

                output_rows.append(new_row)

            # 4. Write final CSV
            with open("carddump_sorted_full.csv", "w", newline="") as f_out:
                fieldnames = output_rows[0].keys()
                writer = csv.DictWriter(f_out, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(output_rows)

        case '3':
            oVector = vector.Vector()