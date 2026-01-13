from bin_tree import BinaryTree
import random
import time
import statistics as stats
from sortedcontainers import SortedSet

def best_case_order(sorted_keys):
    q = [(0, len(sorted_keys) - 1)]
    head = 0
    out = []

    while head < len(q):
        lo, hi = q[head]
        head += 1
        if lo > hi:
            continue
        mid = (lo + hi) // 2
        out.append(sorted_keys[mid])
        q.append((lo, mid - 1))
        q.append((mid + 1, hi))
    return out

def insert_benchmark(tree, keys):
    times = []
    tree = tree()
    t0 = time.perf_counter()
    for k in keys:
        tree.add(k)
        times.append(time.perf_counter() - t0)
    return times

def remove_benchmark(tree, keys):
    tree = tree()
    for k in keys:
        tree.add(k)
    times = []
    t0 = time.perf_counter()
    for k in keys:
        tree.remove(k)
        times.append(time.perf_counter() - t0)
    return times

if __name__ == "__main__":
    m = 17
    n = 2**m - 1
    tree = BinaryTree()
    
    ins_final_rand = []
    ins_final_best = []
    ins_final_set = []
    ins_final_set_best = []
    rm_final_rand = []
    rm_final_set = []

    for _ in range(30):
        rand_keys = random.sample(range(10 * n), n)
        balanced_order = best_case_order(sorted(rand_keys))

        ins_final_rand.append(insert_benchmark(BinaryTree, rand_keys)[-1])
        ins_final_best.append(insert_benchmark(BinaryTree, balanced_order)[-1])
        ins_final_set.append(insert_benchmark(SortedSet, rand_keys)[-1])
        ins_final_set_best.append(insert_benchmark(SortedSet, balanced_order)[-1])
        rm_final_rand.append(remove_benchmark(BinaryTree, rand_keys)[-1])
        rm_final_set.append(remove_benchmark(SortedSet, rand_keys)[-1])

    print("Final insertion time random-order BST:", stats.median(ins_final_rand))
    print("Final insertion time best-case BST:", stats.median(ins_final_best))
    print("Final insertion time random-order SortedSet:", stats.median(ins_final_set))
    print("Final insertion time best-case SortedSet:", stats.median(ins_final_set_best))
    print("Final removal time random-order BST:", stats.median(rm_final_rand))
    print("Final removal time random-order SortedSet:", stats.median(rm_final_set))