from pyspark.sql import SparkSession
import sys
import re

if len(sys.argv) != 2:
    print("Usage: spark-submit spark-word-count.py <input-path>", file=sys.stderr)
    sys.exit(-1)

input_path = sys.argv[1]
output_path = "spark-output-word-count"

spark = SparkSession.builder.appName("WordCount").getOrCreate()
lines = spark.read.text(input_path).rdd.map(lambda r: r[0].lower())
words = lines.flatMap(lambda line: re.findall(r'\b\w+\b', line))
word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
sorted_word_counts = word_counts.sortByKey()

result = sorted_word_counts.map(lambda x: f"{x[0]}\t{x[1]}")
result.coalesce(1).saveAsTextFile(output_path)

spark.stop()
