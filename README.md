# Assignment 5 — Quicksort: Implementation, Analysis, and Randomization

## Contents
- `quicksort.py` — deterministic and randomized in-place Quicksort implementations.
- `benchmark.py` — repeatable timing experiment across random, sorted, and reverse-sorted inputs.
- `benchmark_results.csv` — measured median/minimum/maximum runtimes from the included experiment.
- `runtime_comparison.png` — visualization of median runtimes.
- `report.docx` — formatted Word report for submission.
- `report.md` — editable Markdown source for the report.
- `requirements.txt` — Python dependencies (none required for the algorithms; Matplotlib/Pandas are only needed to regenerate the plot/report artifacts).

## Requirements
Python 3.9 or newer. The implementations and benchmark use only the Python standard library.

## Run the implementation smoke tests
```bash
python quicksort.py
```

## Run the benchmark
```bash
python benchmark.py
```
By default, the experiment uses input sizes 100, 500, 1,000, 2,000, and 5,000; random, sorted, and reverse-sorted distributions; and three repetitions per combination. Results are written to `benchmark_results.csv`. A fixed seed makes the generated inputs reproducible, while runtime measurements naturally vary by machine and system load.

For a smaller/faster run:
```bash
python benchmark.py --sizes 100 500 1000 --repetitions 2 --output quick_test.csv
```

## Summary of findings
Deterministic Quicksort with the final element as pivot is vulnerable to already sorted and reverse-sorted inputs, which create highly unbalanced partitions and quadratic work. Randomized Quicksort chooses a pivot uniformly from the active subarray, making consistently poor splits unlikely and yielding expected `O(n log n)` time. Its worst case remains `O(n^2)`. Actual timing results are in `benchmark_results.csv` and the report; timings are machine-dependent.

## GitHub submission
Create a new repository on GitHub, then upload all files in this folder (or push them with Git). Suggested repository name: `assignment-5-quicksort-analysis`.
