#!/bin/bash

# Assurer que Hadoop et Spark sont dans le PATH
export PATH=$PATH:$(pwd)/hadoop-2.9.1/bin

echo "===================="
echo "DÉBUT : Exécution du script unifié"
echo "===================="

# 1. Exécuter Word Count avec Hadoop
echo "▶ Exécution de Word Count avec Hadoop..."
INPUT_DIR="input-word-count"
OUTPUT_DIR="output-word-count"
hadoop fs -rm -r $OUTPUT_DIR  # Supprimer l'ancien dossier de sortie
hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $INPUT_DIR \
    -output $OUTPUT_DIR \
    -mapper word-count-map.py \
    -reducer word-count-reduce.py
echo "✅ Word Count terminé."
echo "--------------------"

# 2. Exécuter l'analyse Twitter avec Hadoop
echo "▶ Exécution de l'analyse Twitter avec Hadoop..."
INPUT_FILE="social_network.edgelist"
OUTPUT_COUNT="twitter-followers-count"
OUTPUT_AGGREGATES="twitter-aggregates"
hadoop fs -rm -r $OUTPUT_COUNT $OUTPUT_AGGREGATES  # Supprimer les anciens dossiers de sortie
hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $INPUT_FILE \
    -output $OUTPUT_COUNT \
    -mapper twitter-followers-map.py \
    -reducer twitter-followers-reduce.py
hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $OUTPUT_COUNT \
    -output $OUTPUT_AGGREGATES \
    -mapper twitter-aggregates-map.py \
    -reducer twitter-aggregates-reduce.py
echo "✅ Analyse Twitter terminée."
echo "--------------------"

# 3. Exécuter le produit matriciel avec Hadoop (2 rounds)
echo "▶ Exécution du produit matriciel avec Hadoop (2 rounds)..."
INPUT_FILE="input-matmul"
INTERMEDIATE_OUTPUT="matmul-intermediate"
FINAL_OUTPUT="matmul-final"
hadoop fs -rm -r $INTERMEDIATE_OUTPUT $FINAL_OUTPUT  # Supprimer les anciens dossiers de sortie
hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $INPUT_FILE \
    -output $INTERMEDIATE_OUTPUT \
    -mapper matmul-two-rounds-map1.py \
    -reducer matmul-two-rounds-reduce1.py
hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $INTERMEDIATE_OUTPUT \
    -output $FINAL_OUTPUT \
    -mapper matmul-two-rounds-map2.py \
    -reducer matmul-two-rounds-reduce2.py
echo "✅ Produit matriciel (2 rounds) terminé."
echo "--------------------"

# 4. Exécuter le produit matriciel avec Hadoop (1 round)
echo "▶ Exécution du produit matriciel avec Hadoop (1 round)..."
FINAL_OUTPUT_SINGLE="matmul-single-round"
hadoop fs -rm -r $FINAL_OUTPUT_SINGLE  # Supprimer l'ancien dossier de sortie
hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input $INPUT_FILE \
    -output $FINAL_OUTPUT_SINGLE \
    -mapper matmul-single-round-map.py \
    -reducer matmul-single-round-reduce.py
echo "✅ Produit matriciel (1 round) terminé."
echo "--------------------"

# 5. Exécuter les scripts Spark (à la fin)
echo "▶ Exécution des scripts Spark..."
WORD_COUNT_OUTPUT="spark-output-word-count"
TWITTER_OUTPUT="output/twitter-aggregates.txt"
MATRIX_OUTPUT="output-matmul-spark"

# Supprimer les anciens fichiers de sortie
rm -rf $WORD_COUNT_OUTPUT $MATRIX_OUTPUT
rm -f $TWITTER_OUTPUT

echo "  🟢 Exécution de Word Count avec Spark..."
spark-submit word-count-spark.py input-word-count

echo "  🟢 Exécution de l'analyse Twitter avec Spark..."
mkdir -p output
spark-submit twitter_analysis_spark.py social_network.edgelist

echo "  🟢 Exécution du produit matriciel avec Spark..."
spark-submit matmul-spark.py input-matmul output-matmul-spark
echo "✅ Scripts Spark terminés."
echo "--------------------"

echo "===================="
echo "FIN : Exécution du script unifié"
echo "===================="
