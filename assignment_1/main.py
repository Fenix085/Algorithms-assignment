from sorter import *
from vector import Vector
from linked_list import LinkedList
import time
import random
from statistics import median
import csv
import matplotlib.pyplot as plt
import gc

def random_array(n):
    return [random.randint(-50000, 50000) for _ in range(n)]

def measure(algo, n, reps=30):
    times = []
    for _ in range(reps):
        if algo == oSorter.radixSort:
            arr = [random.randint(0, 5000) for _ in range(n)]
        else:
            arr = random_array(n)
        arr_copy = arr[:]
        start = time.perf_counter()
        algo(arr_copy)
        end = time.perf_counter()
        times.append(end - start)
    return median(times)

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

def bench_appends(name, make_container, push_fn, N=2000000, sample_every=50000):
    gc_was_enabled = gc.isenabled()
    gc.disable()

    c = make_container()

    has_cap = hasattr(c, "capacity")
    has_addr = hasattr(c, "buffer_address")

    last_cap = c.capacity() if has_cap else None
    last_addr = c.buffer_address() if has_addr else None

    is_py_list = isinstance(c, list)
    last_size = c.__sizeof__() if is_py_list else None

    realloc_events = []
    samples = []

    t0 = time.perf_counter()
    for i in range(1, N + 1):
        push_fn(c, i)

        if has_cap:
            cap = c.capacity()
            if cap != last_cap:
                realloc_events.append((i, f"cap {last_cap}->{cap}"))
                last_cap = cap

        if has_addr:
            addr = c.buffer_address()
            if addr != last_addr:
                realloc_events.append((i, "addr changed"))
                last_addr = addr

        if is_py_list:
            size = c.__sizeof__()
            if size != last_size:
                realloc_events.append((i, f"__sizeof__ {last_size}->{size}"))
                last_size = size

        if i % sample_every == 0:
            samples.append((i, time.perf_counter() - t0))

    total = time.perf_counter() - t0
    if gc_was_enabled:
        gc.enable()

    print(f"\n{name}")
    print(f"N={N:,} total={total:.3f}s")
    print(f"realloc-events-detected={len(realloc_events)}")
    if realloc_events:
        print("first reallocs:", realloc_events[:10])

    return total, samples, realloc_events

if __name__ == "__main__":

    choice = input("1 - run tests (task1A)\n2 - Olsen Gang (task1B)\n" \
            "3 - for vector implementation\n4 - for racing of data storages\n" \
            "5 - 'Dangerous Quickminds': ")

    oSorter = Sorter()

    match choice.strip():
        case '1':
            sizes = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]
            sizes_long = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]

            version = input("1 - for quick (default), 2 - for long (really long, I did maximum for 10000, it will have to sort array of 50000 elements 30 (or whatever) times (I am looking at you, bubble sort)): ")
            if version.strip() == '2':
                sizes = sizes_long

            results = { 'bubble': [], 'insertion': [], 'merge': [], 'quick': [], 'radix(only non-negative)': [], 'stalin': [], 'communizm': [], 'heap': [] }

            for n in sizes:
                for name, func in [('bubble', oSorter.bubbleSort),
                                ('insertion', oSorter.insertionSort),
                                ('merge', oSorter.mergeSort),
                                ('quick', oSorter.quickSort),
                                ('radix(only non-negative)', oSorter.radixSort),
                                ('stalin', oSorter.stalinSort),
                                ('communizm', oSorter.communizmSort),
                                ('heap', oSorter.heapSort)]:
                    avg = measure(func, n)
                    results[name].append(avg)
                    print(f"{name} n={n}: {avg:.6f} s")
           
            plt.figure()

            plt.plot(sizes, results['bubble'], marker='o', label='Bubble sort')
            plt.plot(sizes, results['insertion'], marker='o', label='Insertion sort')
            plt.plot(sizes, results['merge'], marker='o', label='Merge sort')
            plt.plot(sizes, results['quick'], marker='o', label='Quick sort')
            plt.plot(sizes, results['radix(only non-negative)'], marker='o', label='Radix sort (only non-negative)')
            plt.plot(sizes, results['stalin'], marker='o', label='Stalin sort')
            plt.plot(sizes, results['communizm'], marker='o', label='Communizm sort')
            plt.plot(sizes, results['heap'], marker='o', label='Heap sort')

            plt.xlabel('Array size n')
            plt.ylabel('Average running time (seconds)')
            plt.title('Running time of sorting algorithms')
            plt.legend()
            plt.grid(True)

            plt.show()

            with open("assignment_1/results/sorting_results.csv", "w", newline="") as f:
                writer = csv.writer(f)
                # header
                writer.writerow(["n", "bubble", "insertion", "merge", "quick", "radix(only non-negative)", "stalin", "heap", "communizm"])
                
                # one row per n
                for i, n in enumerate(sizes):
                    writer.writerow([
                        n,
                        results["bubble"][i],
                        results["insertion"][i],
                        results["merge"][i],
                        results["quick"][i],
                        results["radix(only non-negative)"][i],
                        results["stalin"][i],
                        results["communizm"][i],
                        results["heap"][i],
                    ])
        case '2':
            rows = []
            with open("assignment_1/data/carddump2.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)
            
            key_row_dict = { create_key(row): row for row in rows }
            sorted_keys = oSorter.radixSort(list(key_row_dict.keys()))
            rows = [key_row_dict[k] for k in sorted_keys]

            with open("assignment_1/results/carddump2_sorted.csv", "w", newline="") as f:
                filednames = rows[0].keys()
                writer = csv.DictWriter(f, fieldnames=filednames)
                writer.writeheader()
                writer.writerows(rows)

            # 1. Read dump1 (masked last 4)
            with open("assignment_1/data/carddump1.csv", "r", newline="") as f1:
                reader1 = csv.DictReader(f1)
                rows1 = list(reader1)

            # 2. Read sorted dump2 (masked first 12, real last 4)
            with open("assignment_1/results/carddump2_sorted.csv", "r", newline="") as f2:
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
            with open("assignment_1/results/carddump_sorted_full.csv", "w", newline="") as f_out:
                fieldnames = output_rows[0].keys()
                writer = csv.DictWriter(f_out, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(output_rows)

        case '3':
            oVec = Vector()
            done = False
            while not done:
                choice = input("1 - push_back, 2 - resize, 3 - erase, 4 - erase_range, 5- to_list, any other key - exit: ")
                match choice.strip():
                    case '1':
                        val = int(input("Value to push_back: "))
                        oVec.push_back(val)
                        print("Done.")
                    case '2':
                        new_size = int(input("New size: "))
                        fill = int(input("Fill value (default 0): ") or "0")
                        oVec.resize(new_size, fill)
                        print("Done.")
                    case '3':
                        pos = int(input("Position to erase: "))
                        oVec.erase(pos)
                        print("Done.")
                    case '4':
                        start = int(input("Start position to erase_range: "))
                        end = int(input("End position to erase_range: "))
                        oVec.erase_range(start, end)
                        print("Done.")
                    case '5':
                        lst = oVec.to_list()
                        print("Vector contents:", lst)
                    case _:
                        done = True
        case "4":
            bench_appends("Vector", make_container=lambda: Vector(), push_fn = lambda v, x: v.push_back(x))
            bench_appends("Python list", make_container=lambda: [], push_fn = lambda lst, x: lst.append(x))
            bench_appends("LinkedList", make_container=lambda: LinkedList(), push_fn = lambda ll, x: ll.push_back(x))

        case "5":
            sizes = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]

            results = { '1-pivot': [], '2-pivot': [], '3-pivot': [] }

            for n in sizes:
                for name, func in [('1-pivot', oSorter.quickSort),
                                ('2-pivot', oSorter.dualPivotQuickSort),
                                ('3-pivot', oSorter.triplePivotQuickSort)]:
                    avg = measure(func, n)
                    results[name].append(avg)
                    print(f"{name} n={n}: {avg:.6f} s")
           
            plt.figure()

            plt.plot(sizes, results['1-pivot'], marker='o', label='1-pivot Quick sort')
            plt.plot(sizes, results['2-pivot'], marker='o', label='2-pivot Quick sort')
            plt.plot(sizes, results['3-pivot'], marker='o', label='3-pivot Quick sort')

            plt.xlabel('Array size n')
            plt.ylabel('Average running time (seconds)')
            plt.title('Running time of sorting algorithms')
            plt.legend()
            plt.grid(True)

            plt.show()

            with open("assignment_1/results/sorting_results_pivots.csv", "w", newline="") as f:
                writer = csv.writer(f)
                # header
                writer.writerow(["n", "1-pivot", "2-pivot", "3-pivot"])
                
                # one row per n
                for i, n in enumerate(sizes):
                    writer.writerow([
                        n,
                        results["1-pivot"][i],
                        results["2-pivot"][i],
                        results["3-pivot"][i],
                    ])
        
        case 'fuck around':
            sizes = [50000, 100000, 200000, 500000, 1000000]
            
            results = { 'bubble': [], 'insertion': [], 'merge': [], 'quick': [], 'radix(only non-negative)': [], 'stalin': [] }

            for n in sizes:
                for name, func in [('stalin', oSorter.stalinSort)]:
                    avg = measure(func, n)
                    results[name].append(avg)
                    print(f"{name} n={n}: {avg:.6f} s")
                