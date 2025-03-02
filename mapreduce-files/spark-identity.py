import sys
import os
import pyspark

repertoire = sys.argv[1]
fichiers = os.popen("ls " + repertoire).read().strip().split()

sc = pyspark.SparkContext()
sc.setLogLevel("ERROR")

rdd = sc.textFile (repertoire + "/" + fichiers[0])
for i in range(1, len(fichiers)):
  rdd = rdd.union(sc.textFile (repertoire + "/" + fichiers[i]))

for line in rdd.collect():
  print (line)
