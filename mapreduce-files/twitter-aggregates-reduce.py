#!/usr/bin/env python3
import sys

total_users = 0
total_relationships = 0
min_followers = float('inf')
max_followers = 0
min_user = ""
max_user = ""

for line in sys.stdin:
    key, value = line.strip().split('\t')
    
    if key == "total_users":
        total_users += int(value)
    elif key == "total_relationships":
        total_relationships += int(value)
    elif key == "min_followers":
        user, count = value.split(':')
        count = int(count)
        if count < min_followers:
            min_followers = count
            min_user = user
    elif key == "max_followers":
        user, count = value.split(':')
        count = int(count)
        if count > max_followers:
            max_followers = count
            max_user = user

print(f"nb total de relations friend/follower : {total_relationships}")
print(f"nb utilisateurs qui ont au moins un follower : {total_users}")
print(f"nb max de followers par utilisateur : {max_followers} ; par exemple utilisateur : {max_user}")
print(f"nb min de followers par utilisateur : {min_followers} ; par exemple utilisateur : {min_user}")