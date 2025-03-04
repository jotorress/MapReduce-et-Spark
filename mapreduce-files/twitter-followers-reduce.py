#!/usr/bin/env python3
import sys

current_friend = None
current_count = 0

for line in sys.stdin:
    friend, count = line.strip().split('\t')
    count = int(count)
    
    if current_friend == friend:
        current_count += count
    else:
        if current_friend:
            print(f"{current_friend}\t{current_count}")
        current_friend = friend
        current_count = count

if current_friend:
    print(f"{current_friend}\t{current_count}")