#!/bin/bash
# Script pour exécuter l'exercice d'Agrégats sur le Graphe Twitter

# Variables
INPUT_FILE="social_network.edgelist"
OUTPUT_COUNT="twitter-followers-count"
OUTPUT_AGGREGATES="twitter-aggregates"

# Supprimer les répertoires de sortie s'ils existent
hadoop-2.9.1/bin/hadoop fs -rm -r $OUTPUT_COUNT
hadoop-2.9.1/bin/hadoop fs -rm -r $OUTPUT_AGGREGATES

# Premier Round MapReduce
hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $INPUT_FILE \
    -output $OUTPUT_COUNT \
    -mapper twitter-followers-map.py \
    -reducer twitter-followers-reduce.py

# Deuxième Round MapReduce
hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $OUTPUT_COUNT \
    -output $OUTPUT_AGGREGATES \
    -mapper twitter-aggregates-map.py \
    -reducer twitter-aggregates-reduce.py
