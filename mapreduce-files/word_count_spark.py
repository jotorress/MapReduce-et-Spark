#!/usr/bin/env python3

from pyspark import SparkContext
import re
import os
import shutil
import sys

# Verificar si se proporcionó el parámetro de entrada
if len(sys.argv) != 2:
    print("Uso: spark-submit word_count_spark.py <directorio-de-entrada>")
    sys.exit(1)

# Directorio de entrada (pasado como parámetro)
input_dir = sys.argv[1]

# Crear el contexto de Spark
sc = SparkContext("local", "Word Count")

# Leer todos los archivos del directorio pasado como argumento
rdd = sc.textFile(f"{input_dir}/*")

# Transformaciones:
word_counts = (
    rdd.flatMap(lambda line: re.findall(r'\b\w+\b', line.lower()))  # Tokenización y minúsculas
       .map(lambda word: (word, 1))  # Mapeo inicial
       .reduceByKey(lambda a, b: a + b)  # Reducción por clave
       .sortByKey()  # Ordenar alfabéticamente
)

# Crear directorio de salida si no existe
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Guardar en un directorio temporal
temp_output_dir = os.path.join(output_dir, "temp-output-word-count")
word_counts.map(lambda x: f"{x[0]}\t{x[1]}").saveAsTextFile(temp_output_dir)

# Combinar los archivos en uno solo dentro del directorio output
final_output = os.path.join(output_dir, "output-word-count.txt")
with open(final_output, "w") as outfile:
    for part in sorted(os.listdir(temp_output_dir)):
        if part.startswith("part-"):
            with open(os.path.join(temp_output_dir, part), "r") as infile:
                outfile.write(infile.read())

# Eliminar el directorio temporal
shutil.rmtree(temp_output_dir)

# Detener el contexto de Spark
sc.stop()
