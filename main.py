"""Approximate membership via a deterministic mergeable Bloom filter."""
import argparse
import hashlib
import json
import math

class BloomFilter:

    def __init__(self, expected_items=100, false_positive_rate=0.01):
        if type(expected_items) is not int or not 1 <= expected_items <= 1000000:
            raise ValueError('expected_items must be 1..1000000')
        if type(false_positive_rate) not in (int, float) or not math.isfinite(false_positive_rate) or (not 1e-09 <= false_positive_rate < 1):
            raise ValueError('false_positive_rate must be in [1e-9,1)')
        self.bits = max(1, math.ceil(-expected_items * math.log(false_positive_rate) / math.log(2) ** 2))
        self.hashes = max(1, round(self.bits / expected_items * math.log(2)))
        self.data = bytearray((self.bits + 7) // 8)

    def positions(self, value):
        if not isinstance(value, str):
            raise ValueError('Values must be strings')
        digest = hashlib.sha256(value.encode('utf-8')).digest()
        a = int.from_bytes(digest[:16], 'big')
        b = int.from_bytes(digest[16:], 'big') | 1
        return [(a + i * b) % self.bits for i in range(self.hashes)]

    def add(self, value):
        for position in self.positions(value):
            self.data[position // 8] |= 1 << position % 8

    def contains(self, value):
        return all((self.data[p // 8] & 1 << p % 8 for p in self.positions(value)))

    def merge(self, other):
        if not isinstance(other, BloomFilter) or (self.bits, self.hashes) != (other.bits, other.hashes):
            raise ValueError('Filter parameters must match')
        self.data = bytearray((a | b for (a, b) in zip(self.data, other.data)))

    def stats(self):
        return {'bits': self.bits, 'hashes': self.hashes, 'bytes': len(self.data), 'set_bits': sum((bin(b).count('1') for b in self.data))}

def demo():
    f = BloomFilter(100, 0.01)
    for value in ['synthetic-a', 'synthetic-b', 'synthetic-c']:
        f.add(value)
    return {**f.stats(), 'membership': {value: f.contains(value) for value in ['synthetic-a', 'unseen-example']}, 'positive_means': 'possibly present'}
if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(demo(), indent=2))
