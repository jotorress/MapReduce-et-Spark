#!/usr/bin/env python3
#matmul_two_rounds_reduce1.py
import sys
from collections import defaultdict

current_j = None
m_values = []  # Paires (i, value) de la matrice M
n_values = []  # Paires (k, value) de la matrice N

for line in sys.stdin:
    # Analyser la ligne d'entrée
    j, data = line.strip().split('\t')
    
    # Si nous rencontrons une nouvelle clé de jointure, traiter la précédente
    if current_j and current_j != j:
        # Pour chaque paire d'éléments de M et N ayant le même j,
        # émettre un produit partiel avec la clé (i,k)
        for m_i, m_val in m_values:
            for n_k, n_val in n_values:
                # La clé pour le deuxième round sera (i,k)
                # La valeur est le produit partiel M(i,j) * N(j,k)
                partial_product = float(m_val) * float(n_val)
                print(f"{m_i},{n_k}\t{partial_product}")
        
        # Réinitialiser pour la nouvelle clé de jointure
        m_values = []
        n_values = []
    
    current_j = j
    
    # Analyser les données en fonction de la matrice
    parts = data.split(',')
    matrix = parts[0]
    
    if matrix == "M":
        # Stocker (i, value) de M
        m_values.append((parts[1], parts[2]))
    elif matrix == "N":
        # Stocker (k, value) de N
        n_values.append((parts[1], parts[2]))

if current_j:
    for m_i, m_val in m_values:
        for n_k, n_val in n_values:
            partial_product = float(m_val) * float(n_val)
            print(f"{m_i},{n_k}\t{partial_product}")