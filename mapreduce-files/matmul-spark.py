#!/usr/bin/env python3
from pyspark import SparkContext
import sys

# Initialiser le contexte Spark
sc = SparkContext("local", "Multiplication Matricielle")

# Lire les chemins d'entrée et de sortie
input_path = sys.argv[1]
output_path = sys.argv[2]

# Lire les matrices et les transformer en (indice, valeur)
matrix1 = sc.textFile(f"{input_path}/M.txt") \
            .map(lambda line: line.split("|")) \
            .map(lambda parts: ((int(parts[1]), int(parts[2])), float(parts[3])))

matrix2 = sc.textFile(f"{input_path}/N.txt") \
            .map(lambda line: line.split("|")) \
            .map(lambda parts: ((int(parts[1]), int(parts[2])), float(parts[3])))

# Convertir au format de multiplication
M_mapped = matrix1.map(lambda x: (x[0][1], (x[0][0], x[1])))  # Clé = colonne de M
N_mapped = matrix2.map(lambda x: (x[0][0], (x[0][1], x[1])))  # Clé = ligne de N

# Faire la jointure par la clé commune (colonne de M = ligne de N)
joined = M_mapped.join(N_mapped)

# Calculer les produits partiels
product = joined.map(lambda x: ((x[1][0][0], x[1][1][0]), x[1][0][1] * x[1][1][1]))

# Additionner les valeurs avec la même clé (i, k)
result = product.reduceByKey(lambda x, y: x + y)

# Formater le résultat de la multiplication au format i,j\tvaleur
# Convertir les valeurs en entiers si ce sont des nombres naturels
formatted_result = result.map(lambda x: (x[0], int(x[1]) if x[1] == int(x[1]) else x[1])) \
                         .map(lambda x: f"{x[0][0]},{x[0][1]}\t{x[1]}")

# Trier le résultat par (i, j)
sorted_result = formatted_result.sortBy(lambda x: (int(x.split(",")[0]), int(x.split(",")[1].split("\t")[0])))

# Forcer Spark à écrire dans un seul fichier
sorted_result.coalesce(1).saveAsTextFile(output_path)

# Arrêter Spark
sc.stop()
