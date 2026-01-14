from bin_tree import BinaryTree
from tern_tree import TernaryTree
from avl_tree import AVLTree
import random
import time
import statistics as stats
from sortedcontainers import SortedSet

def best_case_order(tree, sorted_keys):
    q = [(0, len(sorted_keys) - 1)]
    head = 0
    out = []
    if tree is BinaryTree or tree is AVLTree:
        while head < len(q):
            lo, hi = q[head]
            head += 1
            if lo > hi:
                continue
            mid = (lo + hi) // 2
            out.append(sorted_keys[mid])
            q.append((lo, mid - 1))
            q.append((mid + 1, hi))

    elif tree is TernaryTree:
        while head < len(q):
            lo, hi = q[head]
            head += 1
            if lo > hi:
                continue

            length = hi - lo + 1

            if length == 1:
                out.append(sorted_keys[lo])
                continue

            if length == 2:
                out.append(sorted_keys[lo])
                out.append(sorted_keys[hi])
                continue

            third_1 = lo + (length) // 3
            third_2 = lo + 2 * (length) // 3

            if third_2 == third_1:
                third_2 += 1

            out.append(sorted_keys[third_1])
            out.append(sorted_keys[third_2])
            q.append((lo, third_1 - 1))
            q.append((third_1 + 1, third_2 - 1))
            q.append((third_2 + 1, hi))
    
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
    ins_final_rand_tern = []
    ins_final_best_tern = []
    ins_final_rand_avl = []
    ins_final_best_avl = []

    for _ in range(30):
        rand_keys = random.sample(range(10 * n), n)
        balanced_order_bin = best_case_order(BinaryTree, sorted(rand_keys))
        balanced_order_tern = best_case_order(TernaryTree, sorted(rand_keys))   

        ins_final_rand.append(insert_benchmark(BinaryTree, rand_keys)[-1])
        ins_final_best.append(insert_benchmark(BinaryTree, balanced_order_bin)[-1])
        ins_final_set.append(insert_benchmark(SortedSet, rand_keys)[-1])
        ins_final_set_best.append(insert_benchmark(SortedSet, balanced_order_bin)[-1])
        rm_final_rand.append(remove_benchmark(BinaryTree, rand_keys)[-1])
        rm_final_set.append(remove_benchmark(SortedSet, rand_keys)[-1])
        ins_final_rand_tern.append(insert_benchmark(TernaryTree, rand_keys)[-1])
        ins_final_best_tern.append(insert_benchmark(TernaryTree, balanced_order_tern)[-1])
        ins_final_rand_avl.append(insert_benchmark(AVLTree, rand_keys)[-1])
        ins_final_best_avl.append(insert_benchmark(AVLTree, balanced_order_bin)[-1])

    print("Final insertion time random-order BST:", stats.median(ins_final_rand))
    print("Final insertion time best-case BST:", stats.median(ins_final_best))
    print("Final insertion time random-order SortedSet:", stats.median(ins_final_set))
    print("Final insertion time best-case SortedSet:", stats.median(ins_final_set_best))
    print("Final removal time random-order BST:", stats.median(rm_final_rand))
    print("Final removal time random-order SortedSet:", stats.median(rm_final_set))
    print("Final insertion time random-order Ternary Tree:", stats.median(ins_final_rand_tern))
    print("Final insertion time best-case Ternary Tree:", stats.median(ins_final_best_tern))
    print("Final insertion time random-order AVL Tree:", stats.median(ins_final_rand_avl))
    print("Final insertion time best-case AVL Tree:", stats.median(ins_final_best_avl))