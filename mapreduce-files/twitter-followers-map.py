#!/usr/bin/env python3
import sys

for line in sys.stdin:
    friend, follower = line.strip().split()
    print(f"{friend}\t1")