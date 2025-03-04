#!/bin/bash
# Script pour exécuter l'exercice de Produit Matriciel avec un seul round

# Variables
INPUT_FILE="input-matmul"
FINAL_OUTPUT="matmul-single-round"

# Supprimer le répertoire de sortie s'il existe
hadoop-2.9.1/bin/hadoop fs -rm -r $FINAL_OUTPUT

# Exécuter MapReduce en un seul round
hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $INPUT_FILE \
    -output $FINAL_OUTPUT \
    -mapper matmul-single-round-map.py \
    -reducer matmul-single-round-reduce.py
