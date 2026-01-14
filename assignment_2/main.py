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
    tree = tree()
    t0 = time.perf_counter()
    for k in keys:
        tree.add(k)
    total = time.perf_counter() - t0

    h = tree.height() if hasattr(tree, "height") else None
    return total, h



def remove_benchmark(tree, keys):
    tree = tree()
    t0 = time.perf_counter()
    for k in keys:
        tree.add(k)
    t0 = time.perf_counter()
    for k in keys:
        tree.remove(k)
    total = time.perf_counter() - t0
    return total

if __name__ == "__main__":
    m = 17
    n = 2**m - 1
    tree = BinaryTree()
    
    ins_final_rand = []
    bin_height_rand = []
    ins_final_best = []
    bin_height_best = []
    ins_final_set = []
    ins_final_set_best = []
    rm_final_rand = []
    rm_final_set = []
    ins_final_rand_tern = []
    tern_height_rand = []
    ins_final_best_tern = []
    tern_height_best = []
    ins_final_rand_avl = []
    avl_height_rand = []
    ins_final_best_avl = []
    avl_height_best = []

    for _ in range(30):
        rand_keys = random.sample(range(10 * n), n)
        
        balanced_order_bin = best_case_order(BinaryTree, sorted(rand_keys))
        balanced_order_tern = best_case_order(TernaryTree, sorted(rand_keys))   

        t, h = insert_benchmark(BinaryTree, rand_keys)
        ins_final_rand.append(t)
        bin_height_rand.append(h)

        t, h = insert_benchmark(BinaryTree, balanced_order_bin)
        ins_final_best.append(t)
        bin_height_best.append(h)

        t, _ = insert_benchmark(SortedSet, rand_keys)
        ins_final_set.append(t)

        t, _ = insert_benchmark(SortedSet, balanced_order_bin)
        ins_final_set_best.append(t)

        t = remove_benchmark(BinaryTree, rand_keys)
        rm_final_rand.append(t)

        t = remove_benchmark(SortedSet, rand_keys)
        rm_final_set.append(t)

        t, h = insert_benchmark(TernaryTree, rand_keys)
        ins_final_rand_tern.append(t)
        tern_height_rand.append(h)

        t, h = insert_benchmark(TernaryTree, balanced_order_tern)
        ins_final_best_tern.append(t)
        tern_height_best.append(h)

        t, h = insert_benchmark(AVLTree, rand_keys)
        ins_final_rand_avl.append(t)
        avl_height_rand.append(h)

        t, h = insert_benchmark(AVLTree, balanced_order_bin)
        ins_final_best_avl.append(t)
        avl_height_best.append(h)


    print("Final insertion time random-order BST:", stats.median(ins_final_rand))
    print("Final BST height random-order:", stats.mean(bin_height_rand))
    print("Final insertion time best-case BST:", stats.median(ins_final_best))
    print("Final BST height best-case:", stats.mean(bin_height_best))
    print("Final insertion time random-order SortedSet:", stats.median(ins_final_set))
    print("Final insertion time best-case SortedSet:", stats.median(ins_final_set_best))
    print("Final removal time random-order BST:", stats.median(rm_final_rand))
    print("Final removal time random-order SortedSet:", stats.median(rm_final_set))
    print("Final insertion time random-order Ternary Tree:", stats.median(ins_final_rand_tern))
    print("Final Ternary Tree height random-order:", stats.mean(tern_height_rand))
    print("Final insertion time best-case Ternary Tree:", stats.median(ins_final_best_tern))
    print("Final Ternary Tree height best-case:", stats.mean(tern_height_best))
    print("Final insertion time random-order AVL Tree:", stats.median(ins_final_rand_avl))
    print("Final AVL Tree height random-order:", stats.mean(avl_height_rand))
    print("Final insertion time best-case AVL Tree:", stats.median(ins_final_best_avl))
    print("Final AVL Tree height best-case:", stats.mean(avl_height_best))