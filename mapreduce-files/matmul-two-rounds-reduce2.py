#!/usr/bin/env python3
# matmul_two_rounds_reduce2.py
import sys

current_key = None
sum_value = 0

for line in sys.stdin:
    # Analyser la ligne d'entrée
    key, value = line.strip().split('\t')
    value = float(value)
    
    # Si nous rencontrons une nouvelle clé, afficher la somme pour la clé précédente
    if current_key and current_key != key:
        # Analyser la ligne et la colonne de la clé
        i, k = current_key.split(',')
        # Afficher dans le format requis : i,k\tvalue (avec un espacement correct)
        print(f"{i},{k}\t {int(sum_value) if sum_value == int(sum_value) else sum_value}")
        sum_value = 0
    
    current_key = key
    sum_value += value

# Ne pas oublier d'afficher la somme pour la dernière clé
if current_key:
    i, k = current_key.split(',')
    print(f"{i},{k}\t {int(sum_value) if sum_value == int(sum_value) else sum_value}")