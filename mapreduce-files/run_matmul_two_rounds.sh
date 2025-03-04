#!/bin/bash
# Script pour exécuter l'exercice de Produit Matriciel avec deux rounds

# Variables
INPUT_FILE="input-matmul"
INTERMEDIATE_OUTPUT="matmul-intermediate"
FINAL_OUTPUT="matmul-final"

# Supprimer les répertoires de sortie s'ils existent
hadoop-2.9.1/bin/hadoop fs -rm -r $INTERMEDIATE_OUTPUT
hadoop-2.9.1/bin/hadoop fs -rm -r $FINAL_OUTPUT

# Premier Round MapReduce
hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $INPUT_FILE \
    -output $INTERMEDIATE_OUTPUT \
    -mapper matmul-two-rounds-map1.py \
    -reducer matmul-two-rounds-reduce1.py

# Deuxième Round MapReduce
hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $INTERMEDIATE_OUTPUT \
    -output $FINAL_OUTPUT \
    -mapper matmul-two-rounds-map2.py \
    -reducer matmul-two-rounds-reduce2.py
