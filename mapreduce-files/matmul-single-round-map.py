#!/usr/bin/env python3
# matmul_single_round_map.py
import sys

for line in sys.stdin:
    # Analyser la ligne d'entrée
    matrix, i, j, value = line.strip().split('|')
    
    if matrix == "M":
        # Pour chaque élément M(i,j), émettre une paire clé-valeur :
        # clé : j (la dimension commune pour la jointure)
        # valeur : M,i,j,value (pour identifier que cela provient de la matrice M)
        print(f"{j}\tM,{i},{j},{value}")
    elif matrix == "N":
        # Pour chaque élément N(j,k), émettre une paire clé-valeur :
        # clé : j (la dimension commune pour la jointure)
        # valeur : N,j,k,value (pour identifier que cela provient de la matrice N)
        print(f"{i}\tN,{i},{j},{value}")