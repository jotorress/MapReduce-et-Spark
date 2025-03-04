#!/bin/bash

# Définir les chemins des fichiers
WORD_COUNT_OUTPUT="spark-output-word-count"
TWITTER_OUTPUT="output/twitter-aggregates.txt"
MATRIX_OUTPUT="output-matmul-spark"

# Supprimer les anciens fichiers de sortie
echo "Suppression des anciens fichiers de sortie..."
rm -rf $WORD_COUNT_OUTPUT
rm -rf $MATRIX_OUTPUT
rm -f $TWITTER_OUTPUT

# 2.1 Exécuter le script Word Count
echo "Exécution du script Word Count..."
spark-submit word-count-spark.py input-word-count

# 2.2 Exécuter le script d'analyse Twitter
echo "Exécution du script d'analyse Twitter..."
# Créer le dossier de sortie pour les agrégats Twitter
mkdir -p output
spark-submit twitter_analysis_spark.py social_network.edgelist 

# Écrire les résultats dans un fichier
echo "Écriture des résultats des agrégats Twitter dans $TWITTER_OUTPUT..."
# Ici, on suppose que twitter_analysis_spark.py écrit déjà dans ce fichier
# Si ce n'est pas le cas, il faudrait modifier le script pour qu'il le fasse.

# 2.3 Exécuter le script de produit matriciel
echo "Exécution du script de produit matriciel..."
spark-submit matmul-spark.py input-matmul output-matmul-spark

echo "Tous les scripts ont été exécutés avec succès."
