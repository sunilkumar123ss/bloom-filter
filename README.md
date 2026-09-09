# Bloom filter membership

Provide bounded approximate membership with mergeable bit arrays.

Educational implementation with synthetic examples.

## Run

Python 3.9 or newer; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

The default example uses synthetic data and needs no credentials, installation, or network connection. The script also works by absolute path from another working directory.

## Behavior

Expected item count and target false-positive probability choose bit count and hash count. SHA-256-derived double hashing sets and checks bits. Compatible filters can merge by bitwise OR, preserving membership of both inputs.

## Use in Python

```python
from main import BloomFilter

filter = BloomFilter(expected_items=1000, false_positive_rate=0.01)
filter.add('example-key')
assert filter.contains('example-key')
# Check positive results against the authoritative collection.
```

## Design limits

A positive result may be a false positive and must be checked against an authoritative store. The target probability assumes a suitable hash distribution and item load; exceeding the planned load increases false positives. This is not a deletion-capable structure, authentication control, or measured production accuracy claim.

## Verification

The unit tests cover successful operations, failure paths, and invariants. These are local correctness checks, not production performance or security certification.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
