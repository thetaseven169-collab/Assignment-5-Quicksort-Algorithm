"""Benchmark deterministic and randomized Quicksort on multiple distributions."""
from __future__ import annotations

import argparse
import csv
import random
import statistics
import time
from pathlib import Path

from quicksort import quicksort, randomized_quicksort

SIZES_DEFAULT = [100, 500, 1000, 2000, 5000]
DISTRIBUTIONS = ("random", "sorted", "reverse-sorted")


def make_input(size: int, distribution: str, seed: int) -> list[int]:
    rng = random.Random(seed)
    if distribution == "random":
        return [rng.randrange(0, max(10, size * 10)) for _ in range(size)]
    if distribution == "sorted":
        return list(range(size))
    if distribution == "reverse-sorted":
        return list(range(size - 1, -1, -1))
    raise ValueError(f"Unknown distribution: {distribution}")


def time_one(sorter, data: list[int], seed: int) -> float:
    work = data.copy()
    rng = random.Random(seed)
    start = time.perf_counter()
    if sorter is randomized_quicksort:
        sorter(work, rng=rng)
    else:
        sorter(work)
    elapsed = time.perf_counter() - start
    if work != sorted(data):
        raise AssertionError(f"{sorter.__name__} produced incorrect output")
    return elapsed


def run_benchmarks(sizes=SIZES_DEFAULT, repetitions: int = 3, seed: int = 2026):
    rows = []
    for size in sizes:
        for distribution in DISTRIBUTIONS:
            source = make_input(size, distribution, seed + size)
            for sorter in (quicksort, randomized_quicksort):
                samples = [
                    time_one(sorter, source, seed + rep * 101 + size)
                    for rep in range(repetitions)
                ]
                rows.append({
                    "algorithm": sorter.__name__,
                    "distribution": distribution,
                    "n": size,
                    "repetitions": repetitions,
                    "median_seconds": statistics.median(samples),
                    "min_seconds": min(samples),
                    "max_seconds": max(samples),
                })
                print(
                    f"{sorter.__name__:22s} {distribution:15s} "
                    f"n={size:5d} median={statistics.median(samples):.6f}s"
                )
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", nargs="+", type=int, default=SIZES_DEFAULT)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--output", default="benchmark_results.csv")
    args = parser.parse_args()
    if args.repetitions < 1 or any(size < 0 for size in args.sizes):
        parser.error("repetitions must be >= 1 and sizes must be >= 0")
    rows = run_benchmarks(args.sizes, args.repetitions, args.seed)
    output = Path(args.output)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved {len(rows)} benchmark rows to {output.resolve()}")


if __name__ == "__main__":
    main()
