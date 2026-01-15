from bin_tree import BinaryTree
from tern_tree import TernaryTree
from avl_tree import AVLTree
import random
import time
import csv
import os
import statistics as stats
from sortedcontainers import SortedSet
import matplotlib.pyplot as plt


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

            third_1 = lo + length // 3
            third_2 = lo + 2 * length // 3

            if third_2 == third_1:
                third_2 += 1

            out.append(sorted_keys[third_1])
            out.append(sorted_keys[third_2])
            q.append((lo, third_1 - 1))
            q.append((third_1 + 1, third_2 - 1))
            q.append((third_2 + 1, hi))

    return out


def insert_benchmark(tree_cls, keys):
    tree = tree_cls()
    t0 = time.perf_counter()
    for k in keys:
        tree.add(k)
    total = time.perf_counter() - t0

    h = tree.height() if hasattr(tree, "height") else None
    return total, h


def remove_benchmark(tree_cls, keys):
    tree = tree_cls()
    for k in keys:
        tree.add(k)

    t0 = time.perf_counter()
    for k in keys:
        tree.remove(k)
    total = time.perf_counter() - t0
    return total


def _quartiles(values):
    vals = [v for v in values if v is not None]
    if len(vals) < 2:
        return None, None
    # stats.quantiles returns [Q1, Q2, Q3] when n=4
    q = stats.quantiles(vals, n=4, method="inclusive")
    return q[0], q[2]


def summarize(values):
    vals = [v for v in values if v is not None]
    if not vals:
        return {
            "count": 0, "median": None, "mean": None, "stdev": None,
            "min": None, "max": None, "q1": None, "q3": None
        }

    q1, q3 = _quartiles(vals)
    return {
        "count": len(vals),
        "median": stats.median(vals),
        "mean": stats.mean(vals),
        "stdev": stats.stdev(vals) if len(vals) >= 2 else 0.0,
        "min": min(vals),
        "max": max(vals),
        "q1": q1,
        "q3": q3,
    }


def save_trials_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_summary_csv(metric_to_values, path):
    rows = []
    for metric, vals in metric_to_values.items():
        s = summarize(vals)
        rows.append({"metric": metric, **s})

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def boxplot(metric_to_values, title, ylabel, path):
    labels = list(metric_to_values.keys())
    data = [metric_to_values[k] for k in labels]

    plt.figure(figsize=(13, 6))
    plt.boxplot(data, labels=labels, showmeans=True)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


if __name__ == "__main__":
    trials = 100
    m = 17
    n = 2**m - 1

    # store per-trial rows (best for CSV + plots)
    rows = []

    # also store lists per metric (best for summaries + plots)
    metrics = {
        "BST insert random (s)": [],
        "BST height random": [],
        "BST insert best (s)": [],
        "BST height best": [],

        "SortedSet insert random (s)": [],
        "SortedSet insert best (s)": [],

        "BST remove random (s)": [],
        "SortedSet remove random (s)": [],

        "Ternary insert random (s)": [],
        "Ternary height random": [],
        "Ternary insert best (s)": [],
        "Ternary height best": [],

        "AVL insert random (s)": [],
        "AVL height random": [],
        "AVL insert best (s)": [],
        "AVL height best": [],
    }

    for trial in range(1, trials + 1):
        rand_keys = random.sample(range(10 * n), n)
        sorted_keys = sorted(rand_keys)

        balanced_order_bin = best_case_order(BinaryTree, sorted_keys)
        balanced_order_tern = best_case_order(TernaryTree, sorted_keys)

        bst_rand_t, bst_rand_h = insert_benchmark(BinaryTree, rand_keys)
        bst_best_t, bst_best_h = insert_benchmark(BinaryTree, balanced_order_bin)

        ss_rand_t, _ = insert_benchmark(SortedSet, rand_keys)
        ss_best_t, _ = insert_benchmark(SortedSet, balanced_order_bin)

        bst_rm_t = remove_benchmark(BinaryTree, rand_keys)
        ss_rm_t = remove_benchmark(SortedSet, rand_keys)

        tern_rand_t, tern_rand_h = insert_benchmark(TernaryTree, rand_keys)
        tern_best_t, tern_best_h = insert_benchmark(TernaryTree, balanced_order_tern)

        avl_rand_t, avl_rand_h = insert_benchmark(AVLTree, rand_keys)
        avl_best_t, avl_best_h = insert_benchmark(AVLTree, balanced_order_bin)

        row = {
            "trial": trial,
            "n": n,

            "bst_insert_random_s": bst_rand_t,
            "bst_height_random": bst_rand_h,
            "bst_insert_best_s": bst_best_t,
            "bst_height_best": bst_best_h,

            "sortedset_insert_random_s": ss_rand_t,
            "sortedset_insert_best_s": ss_best_t,

            "bst_remove_random_s": bst_rm_t,
            "sortedset_remove_random_s": ss_rm_t,

            "ternary_insert_random_s": tern_rand_t,
            "ternary_height_random": tern_rand_h,
            "ternary_insert_best_s": tern_best_t,
            "ternary_height_best": tern_best_h,

            "avl_insert_random_s": avl_rand_t,
            "avl_height_random": avl_rand_h,
            "avl_insert_best_s": avl_best_t,
            "avl_height_best": avl_best_h,
        }
        rows.append(row)

        # push into metric lists
        metrics["BST insert random (s)"].append(bst_rand_t)
        metrics["BST height random"].append(bst_rand_h)
        metrics["BST insert best (s)"].append(bst_best_t)
        metrics["BST height best"].append(bst_best_h)

        metrics["SortedSet insert random (s)"].append(ss_rand_t)
        metrics["SortedSet insert best (s)"].append(ss_best_t)

        metrics["BST remove random (s)"].append(bst_rm_t)
        metrics["SortedSet remove random (s)"].append(ss_rm_t)

        metrics["Ternary insert random (s)"].append(tern_rand_t)
        metrics["Ternary height random"].append(tern_rand_h)
        metrics["Ternary insert best (s)"].append(tern_best_t)
        metrics["Ternary height best"].append(tern_best_h)

        metrics["AVL insert random (s)"].append(avl_rand_t)
        metrics["AVL height random"].append(avl_rand_h)
        metrics["AVL insert best (s)"].append(avl_best_t)
        metrics["AVL height best"].append(avl_best_h)

    out_dir = os.path.abspath(".")
    trials_csv = os.path.join(out_dir, "assignment_2/results/results_trials.csv")
    summary_csv = os.path.join(out_dir, "assignment_2/results/results_summary.csv")

    save_trials_csv(rows, trials_csv)
    save_summary_csv(metrics, summary_csv)

    # Plots (boxplots are nice because they show spread across 30 trials)
    boxplot(
        {
            "BST rnd": metrics["BST insert random (s)"],
            "BST best": metrics["BST insert best (s)"],
            "SortedSet rnd": metrics["SortedSet insert random (s)"],
            "SortedSet best": metrics["SortedSet insert best (s)"],
            "Ternary rnd": metrics["Ternary insert random (s)"],
            "Ternary best": metrics["Ternary insert best (s)"],
            "AVL rnd": metrics["AVL insert random (s)"],
            "AVL best": metrics["AVL insert best (s)"],
        },
        title=f"Insertion times over {trials} trials (n={n})",
        ylabel="seconds",
        path=os.path.join(out_dir, "assignment_2/results/insert_times_boxplot.png"),
    )

    boxplot(
        {
            "BST rnd": metrics["BST height random"],
            "BST best": metrics["BST height best"],
            "Ternary rnd": metrics["Ternary height random"],
            "Ternary best": metrics["Ternary height best"],
            "AVL rnd": metrics["AVL height random"],
            "AVL best": metrics["AVL height best"],
        },
        title=f"Tree heights over {trials} trials (n={n})",
        ylabel="height",
        path=os.path.join(out_dir, "assignment_2/results/heights_boxplot.png"),
    )

    boxplot(
        {
            "BST remove rnd": metrics["BST remove random (s)"],
            "SortedSet remove rnd": metrics["SortedSet remove random (s)"],
        },
        title=f"Removal times over {trials} trials (n={n})",
        ylabel="seconds",
        path=os.path.join(out_dir, "assignment_2/results/remove_times_boxplot.png"),
    )

    # Minimal console output so you know where things landed
    print("Saved:", trials_csv)
    print("Saved:", summary_csv)
    print("Saved:", os.path.join(out_dir, "assignment_2/results/insert_times_boxplot.png"))
    print("Saved:", os.path.join(out_dir, "assignment_2/results/heights_boxplot.png"))
    print("Saved:", os.path.join(out_dir, "assignment_2/results/remove_times_boxplot.png"))