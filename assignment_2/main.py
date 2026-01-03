from bin_tree import BinaryTree
import random
import time
import statistics as stats

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
    t0 = time.perf_counter()
    times = []
    tree = tree()
    for k in keys:
        tree.add(k)
        times.append(time.perf_counter() - t0)
    return times

if __name__ == "__main__":
    m = 17
    n = 2**m - 1
    tree = BinaryTree()
    
      

    final_rand = []
    final_best = []

    for _ in range(30):
        rand_keys = random.sample(range(10 * n), n)
        balanced_order = best_case_order(sorted(rand_keys))

        final_rand.append(insert_benchmark(BinaryTree, rand_keys)[-1])
        final_best.append(insert_benchmark(BinaryTree, balanced_order)[-1])

    print("Final time random-order BST:", stats.median(final_rand))
    print("Final time best-case BST:", stats.median(final_best))
