#!/usr/bin/env python3
# matmul_single_round_reduce.py
import sys
from collections import defaultdict

# Dictionnaire pour collecter les produits partiels
result = defaultdict(float)

current_j = None
m_elements = []  # Stocker les éléments de M
n_elements = []  # Stocker les éléments de N

for line in sys.stdin:
    # Analyser la ligne d'entrée
    j, data = line.strip().split('\t')
    
    # Si nous rencontrons une nouvelle clé de jointure, traiter le lot précédent
    if current_j and current_j != j:
        # Pour chaque paire d'éléments de M et N partageant le même j,
        # calculer le produit partiel et l'ajouter au résultat
        for m_data in m_elements:
            m_parts = m_data.split(',')
            m_i = m_parts[1]
            m_value = float(m_parts[3])
            
            for n_data in n_elements:
                n_parts = n_data.split(',')
                n_k = n_parts[2]
                n_value = float(n_parts[3])
                
                # Ajouter le produit partiel au résultat pour la cellule (i,k)
                result[(m_i, n_k)] += m_value * n_value
        
        # Réinitialiser pour la nouvelle clé de jointure
        m_elements = []
        n_elements = []
    
    current_j = j
    
    # Analyser et stocker les données en fonction de la matrice
    parts = data.split(',')
    matrix = parts[0]
    
    if matrix == "M":
        m_elements.append(data)
    elif matrix == "N":
        n_elements.append(data)

# Traiter le dernier lot
if current_j:
    for m_data in m_elements:
        m_parts = m_data.split(',')
        m_i = m_parts[1]
        m_value = float(m_parts[3])
        
        for n_data in n_elements:
            n_parts = n_data.split(',')
            n_k = n_parts[2]
            n_value = float(n_parts[3])
            
            # Ajouter le produit partiel au résultat pour la cellule (i,k)
            result[(m_i, n_k)] += m_value * n_value

# Afficher le résultat final dans le format requis
for (i, k), value in sorted(result.items()):
    # Convertir en entier si c'est un nombre entier
    formatted_value = int(value) if value == int(value) else value
    print(f"{i},{k}\t {formatted_value}")