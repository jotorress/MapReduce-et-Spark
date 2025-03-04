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

Voici la suite du format demandé pour les exercices, en suivant la même structure :

---

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

### 1.2 Agrégats sur le graphe Twitter
- **Objectif** : Analyser un graphe Twitter pour calculer des agrégats tels que le nombre total d'utilisateurs, le nombre total de relations, et les valeurs minimale et maximale de followers par utilisateur.
- **Scripts** :
  - **Premier Round MapReduce** : Compter le nombre de followers par utilisateur.
    - `twitter-followers-map.py` :
      ```python
      #!/usr/bin/env python3
      import sys
      for line in sys.stdin:
          friend, follower = line.strip().split()
          print(f"{friend}\t1")
      ```
    - `twitter-followers-reduce.py` :
      ```python
        #!/usr/bin/env python3
        import sys
        
        current_friend = None
        current_count = 0
        
        for line in sys.stdin:
            friend, count = line.strip().split('\t')
            count = int(count)
            
            if current_friend == friend:
                current_count += count
            else:
                if current_friend:
                    print(f"{current_friend}\t{current_count}")
                current_friend = friend
                current_count = count
        
        if current_friend:
            print(f"{current_friend}\t{current_count}")
      ```
    - **Exécution** :
      ```bash
      hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
      -input social_network.edgelist \
      -output twitter-followers-count \
      -mapper twitter-followers-map.py \
      -reducer twitter-followers-reduce.py
      ```

  - **Deuxième Round MapReduce** : Calculer les agrégats sur les résultats du premier round.
    - `twitter-aggregates-map.py` :
      ```python
      #!/usr/bin/env python3
      import sys
      for line in sys.stdin:
          friend, count = line.strip().split('\t')
          print(f"total_users\t1")
          print(f"total_relationships\t{count}")
          print(f"min_followers\t{count}")
          print(f"max_followers\t{count}")
      ```
    - `twitter-aggregates-reduce.py` :
      ```python
      #!/usr/bin/env python3
        import sys
        total_users = 0
        total_relationships = 0
        min_followers = float('inf')
        max_followers = 0
        min_user = ""
        max_user = ""
        
        for line in sys.stdin:
            key, value = line.strip().split('\t')
            
            if key == "total_users":
                total_users += int(value)
            elif key == "total_relationships":
                total_relationships += int(value)
            elif key == "min_followers":
                user, count = value.split(':')
                count = int(count)
                if count < min_followers:
                    min_followers = count
                    min_user = user
            elif key == "max_followers":
                user, count = value.split(':')
                count = int(count)
                if count > max_followers:
                    max_followers = count
                    max_user = user
      print(f"nb total de relations friend/follower : {total_relationships}")
      print(f"nb utilisateurs qui ont au moins un follower : {total_users}")
      print(f"nb max de followers par utilisateur : {max_followers} ; par exemple utilisateur : {max_user}")
      print(f"nb min de followers par utilisateur : {min_followers} ; par exemple utilisateur : {min_user}")
      ```
    - **Exécution** :
      ```bash
      hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
      -input twitter-followers-count \
      -output twitter-aggregates \
      -mapper twitter-aggregates-map.py \
      -reducer twitter-aggregates-reduce.py
      ```

---

### 1.3 Produit matriciel
- **Objectif** : Implémenter le produit matriciel en utilisant MapReduce, en deux versions : avec deux rounds MapReduce et avec un seul round.


---

### 2. Spark
- **Objectif** : Réaliser les mêmes tâches (Word Count, Agrégats sur Twitter, Produit matriciel) en utilisant Spark.

#### 2.1 Word Count avec Spark
submit spark-word-count.py
  ```

#### 2.2 Agrégats sur Twitter avec Spark


#### 2.3 Produit matriciel avec Spark


