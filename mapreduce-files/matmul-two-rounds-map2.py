#!/usr/bin/env python3
# matmul_two_rounds_map2.py
import sys

# Le deuxième mapper est un simple mapper d'identité
# Il transmet simplement la sortie du premier reducer
for line in sys.stdin:
    print(line.strip())