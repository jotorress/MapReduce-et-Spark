#!/usr/bin/env python3
#matmul_two_rounds_map1.py
import sys

for line in sys.stdin:
    # Analyser la ligne d'entrée
    parts = line.strip().split('|')
    matrix, row, col, value = parts[0], parts[1], parts[2], parts[3]
    
    if matrix == "M":
        # Pour chaque élément M(i,j), émettre (j, "M,i,value")
        # Cela permettra au reducer de faire correspondre avec les éléments de N ayant le même j
        print(f"{col}\tM,{row},{value}")
    elif matrix == "N":
        # Pour chaque élément N(j,k), émettre (j, "N,k,value")
        print(f"{row}\tN,{col},{value}")