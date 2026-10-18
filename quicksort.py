"""
Assignment 5: Quicksort Algorithm — Implementation, Analysis, and Randomization

Contains deterministic and randomized in-place Quicksort implementations.
Both use Lomuto-style partitioning and recurse only into the smaller partition,
then iterate over the larger partition to keep Python call-stack use bounded.
"""
from __future__ import annotations

import random
from typing import MutableSequence, Optional, TypeVar

T = TypeVar("T")


def _partition(values: MutableSequence[T], low: int, high: int) -> int:
    """Partition around the final element; return its final index."""
    pivot = values[high]
    boundary = low - 1
    for scan in range(low, high):
        if values[scan] <= pivot:
            boundary += 1
            values[boundary], values[scan] = values[scan], values[boundary]
    pivot_index = boundary + 1
    values[pivot_index], values[high] = values[high], values[pivot_index]
    return pivot_index


def quicksort(values: MutableSequence[T]) -> MutableSequence[T]:
    """
    Sort a mutable sequence in place using deterministic Quicksort.
    The last element of each current subarray is selected as the pivot.

    Average/best time: O(n log n); worst time: O(n^2).
    Auxiliary stack: O(log n) with smaller-side recursion; O(n) partition
    stack depth is avoided, although work can still be quadratic.
    """
    def sort(low: int, high: int) -> None:
        while low < high:
            pivot_index = _partition(values, low, high)
            # Recurse on the smaller side; iterate on the larger side.
            if pivot_index - low < high - pivot_index:
                sort(low, pivot_index - 1)
                low = pivot_index + 1
            else:
                sort(pivot_index + 1, high)
                high = pivot_index - 1

    if len(values) > 1:
        sort(0, len(values) - 1)
    return values


def randomized_quicksort(
    values: MutableSequence[T],
    *,
    rng: Optional[random.Random] = None,
) -> MutableSequence[T]:
    """
    Sort a mutable sequence in place using randomized Quicksort.
    A pivot is selected uniformly at random from each active subarray.

    Expected time: O(n log n); worst-case time remains O(n^2), but the
    probability of repeatedly choosing extremely unbalanced pivots is low.
    Pass a random.Random instance to make runs reproducible.
    """
    generator = rng if rng is not None else random

    def sort(low: int, high: int) -> None:
        while low < high:
            chosen = generator.randint(low, high)
            values[chosen], values[high] = values[high], values[chosen]
            pivot_index = _partition(values, low, high)
            if pivot_index - low < high - pivot_index:
                sort(low, pivot_index - 1)
                low = pivot_index + 1
            else:
                sort(pivot_index + 1, high)
                high = pivot_index - 1

    if len(values) > 1:
        sort(0, len(values) - 1)
    return values


if __name__ == "__main__":
    examples = [
        [9, 3, 7, 1, 8, 2],
        [],
        [5],
        [4, 4, 4, 4],
    ]
    for example in examples:
        expected = sorted(example)
        quicksort(example)
        assert example == expected
    print("Quicksort smoke tests passed.")
