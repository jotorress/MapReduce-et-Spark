#!/bin/bash
# Script pour exécuter l'exercice de Compte de Mots

# Variables
INPUT_DIR="input-word-count"
OUTPUT_DIR="output-word-count"

# Supprimer le répertoire de sortie s'il existe
hadoop-2.9.1/bin/hadoop fs -rm -r $OUTPUT_DIR

# Exécuter MapReduce
hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $INPUT_DIR \
    -output $OUTPUT_DIR \
    -mapper word-count-map.py \
    -reducer word-count-reduce.py
