# Rapport : MapReduce et Spark
**Fait par : CHICA Miller et TORRES Jonathan**


## Introduction
Ce document explique l'utilisation de MapReduce avec Hadoop Streaming et Spark pour traiter de grandes quantités de données.

## Préparation de l'environnement (MapReduce)
### Installation et configuration de Hadoop
1. Installer Java :
    ```bash
    sudo apt-get install openjdk-21-jre-headless
    ```
2. Configurer la variable JAVA_HOME :
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
    ```
3. Télécharger et extraire Hadoop :
    ```bash
    tar -xvzf hadoop-2.9.1.tar.gz
    cd hadoop-2.9.1
    ```

### Exécution de MapReduce avec Hadoop Streaming
Commande pour exécuter Hadoop en mode streaming :
```bash
bin/hadoop jar share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
    -input INPUT_DIR \
    -output OUTPUT_DIR \
    -mapper map.py \
    -reducer reduce.py
```

## 1. Exercices
### 1.1 Word Count
- **Objectif** : Compter le nombre d'occurrences des mots en supprimant la ponctuation et en mettant en minuscules.
- **Scripts** :
  - `word-count-map.py` :
    ```python
    #!/usr/bin/env python3
    import sys
    import re
    for line in sys.stdin:
        words = re.findall(r'\b\w+\b', line.lower())
        for word in words:
            print(f"{word}\t1")
    ```
  - `word-count-reduce.py` :
    ```python
    #!/usr/bin/env python3
    import sys
    from collections import defaultdict
    word_counts = defaultdict(int)
    for line in sys.stdin:
        word, count = line.strip().split('\t')
        word_counts[word] += int(count)
    for word, count in word_counts.items():
        print(f"{word}\t{count}")
    ```
- **Exécution** :
   ```bash
   hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
   -input input-word-count \
   -output output-word-count \
   -mapper word-count-map.py \
   -reducer word-count-reduce.py
   ```


---

