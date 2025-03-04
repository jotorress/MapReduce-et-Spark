#!/usr/bin/env python3
import sys

for line in sys.stdin:
    friend, count = line.strip().split('\t')
    count = int(count)
    
    print(f"total_users\t1")
    print(f"total_relationships\t{count}")
    
    print(f"min_followers\t{friend}:{count}")
    print(f"max_followers\t{friend}:{count}")