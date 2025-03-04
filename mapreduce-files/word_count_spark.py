#!/usr/bin/env python3

# Importation des bibliothèques nécessaires
from pyspark import SparkContext
import re
import os
import shutil
import sys

# Vérifier si le paramètre d'entrée est fourni
# Le script doit être exécuté avec : spark-submit word_count_spark.py <dossier-d'entrée>
if len(sys.argv) != 2:
    print("Utilisation : spark-submit word_count_spark.py <dossier-d'entrée>")
    sys.exit(1)

# Dossier d'entrée (fourni en tant que paramètre)
input_dir = sys.argv[1]

# Créer le contexte Spark
sc = SparkContext("local", "Word Count")

# Lire tous les fichiers du dossier fourni en paramètre
rdd = sc.textFile(f"{input_dir}/*")

# Transformations :
word_counts = (
    rdd.flatMap(lambda line: re.findall(r'\b\w+\b', line.lower()))  # Tokenisation et conversion en minuscules
       .map(lambda word: (word, 1))  # Création de paires (mot, 1)
       .reduceByKey(lambda a, b: a + b)  # Réduction par clé pour compter les occurrences
       .sortByKey()  # Trier les mots par ordre alphabétique
)

# Créer un dossier de sortie s'il n'existe pas
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Enregistrer les résultats dans un dossier temporaire
temp_output_dir = os.path.join(output_dir, "temp-output-word-count")
word_counts.map(lambda x: f"{x[0]}\t{x[1]}").saveAsTextFile(temp_output_dir)

# Combiner les fichiers temporaires en un seul fichier dans le dossier output
final_output = os.path.join(output_dir, "output-word-count.txt")
with open(final_output, "w") as outfile:
    for part in sorted(os.listdir(temp_output_dir)):
        if part.startswith("part-"):
            with open(os.path.join(temp_output_dir, part), "r") as infile:
                outfile.write(infile.read())

# Supprimer le dossier temporaire après la combinaison des fichiers
shutil.rmtree(temp_output_dir)

# Arrêter le contexte Spark
sc.stop()
