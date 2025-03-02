#!/usr/bin/env python3
import sys
from collections import defaultdict
word_counts = defaultdict(int)
for line in sys.stdin:
    word, count = line.strip().split('\t')
    word_counts[word] += int(count)
for word, count in word_counts.items():
    print(f"{word}\t{count}")