#!/usr/bin/env python3

from pyspark import SparkContext
import sys
import os
import shutil

# Vérifier si le paramètre d'entrée est fourni
if len(sys.argv) != 2:
    print("Utilisation : spark-submit twitter_analysis_spark.py <fichier-d'entrée>")
    sys.exit(1)

# Dossier d'entrée (fichier d'edges)
input_file = sys.argv[1]

# Créer le contexte Spark
sc = SparkContext("local", "Twitter Analysis")

# Lire le fichier d'entrée
rdd = sc.textFile(input_file)

# Compter le nombre de followers par utilisateur
followers_count = (
    rdd.map(lambda line: tuple(line.strip().split()))  # Diviser les lignes en (friend, follower)
       .map(lambda parts: (parts[0], 1))  # Mapper (ami, 1)
       .reduceByKey(lambda a, b: a + b)  # Réduire par clé pour compter les followers
)

# Calculer les agrégats :
total_users = followers_count.count()  # Nombre d'utilisateurs avec au moins un follower
total_relationships = followers_count.map(lambda x: x[1]).sum()  # Total des relations friend/follower

# Trouver le min et le max des followers
# Utilisation d'une logique avancée pour résoudre le problème du min_user
min_followers = followers_count.reduce(lambda x, y: x if (x[1] < y[1]) or (x[1] == y[1] and x[0] < y[0]) else y)
max_followers = followers_count.reduce(lambda x, y: x if (x[1] > y[1]) or (x[1] == y[1] and x[0] < y[0]) else y)

# Créer un dossier de sortie
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Écrire les résultats dans un fichier
output_file = os.path.join(output_dir, "twitter-aggregates.txt")
with open(output_file, "w") as f:
    f.write(f"nb total de relations friend/follower : {int(total_relationships)}\n")
    f.write(f"nb utilisateurs qui ont au moins un follower : {total_users}\n")
    f.write(f"nb max de followers par utilisateur : {max_followers[1]} ; par exemple utilisateur : {max_followers[0]}\n")
    f.write(f"nb min de followers par utilisateur : {min_followers[1]} ; par exemple utilisateur : {min_followers[0]}\n")

# Arrêter le contexte Spark
sc.stop()
