# Rapport : MapReduce et Spark
**Fait par : CHICA Miller et TORRES Jonathan**


## Introduction
Ce document explique l'utilisation de MapReduce avec Hadoop Streaming et Spark pour traiter de grandes quantités de données.
**Tous les scripts doivent être exécutés à l'intérieur du dossier `mapreduce-files`.**

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
- **Exécution directe** :
   ```bash
   hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
   -input input-word-count \
   -output output-word-count \
   -mapper word-count-map.py \
   -reducer word-count-reduce.py
   ```
- **Exécution avec un script `.sh`** :  
  Vous pouvez également exécuter cette tâche en utilisant un script `.sh`. Avec le fichier `run_word_count.sh` :
  ```bash
  chmod +x run_word_count.sh
  chmod +x *.sh
  ./run_word_count.sh
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
            count = int(count)
            
            print(f"total_users\t1")
            print(f"total_relationships\t{count}")
            
            print(f"min_followers\t{friend}:{count}")
            print(f"max_followers\t{friend}:{count}")
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
                if count < min_followers or (count == min_followers and user < min_user):
                    min_followers = count
                    min_user = user
            elif key == "max_followers":
                user, count = value.split(':')
                count = int(count)
                if count > max_followers or (count == max_followers and user < max_user):
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
    - **Exécution avec un script `.sh`** :  
      Vous pouvez également exécuter cette tâche en utilisant un script `.sh`. Avec le fichier `run_twitter_aggregates.sh` :
      ```bash
      chmod +x *.sh
      ./run_twitter_aggregates.sh
      ``` 
---

### 1.3 Produit matriciel
- **Objectif** : Implémenter le produit matriciel en utilisant MapReduce, en deux versions : avec deux rounds MapReduce et avec un seul round.
- **Scripts** :
  - **Version avec deux rounds MapReduce** :
    Cette version divise le calcul en deux étapes :
    - **Round 1** : Préparer les produits partiels en utilisant les colonnes de M et les lignes de N ayant le même index.
        - **Mapper** (matmul-two-rounds-map1.py): Transforme les lignes d'entrée en paires clé-valeur basées sur les indices des matrices.
        - **Reducer**  (matmul-two-rounds-reduce1.py): Combine les paires basées sur la clé commune et génère des produits partiels.
     
    - **Round 2** : Agréger ces produits partiels pour obtenir le produit final.
        - **Mapper** (matmul-two-rounds-map2.py): Transmet simplement les résultats intermédiaires sans transformation.
        - **Reducer** (matmul-two-rounds-reduce2.py): Additionne les produits partiels pour chaque cellule de la matrice résultante.
      - `matmul-two-rounds-map1.py` :
        ```python
            #!/usr/bin/env python3
            #matmul_two_rounds_map1.py
            import sys
            
            for line in sys.stdin:
                # Analyser la ligne d'entrée
                parts = line.strip().split('|')
                matrix, row, col, value = parts[0], parts[1], parts[2], parts[3]
                
                if matrix == "M":
                    # Pour chaque élément M(i,j), émettre (j, "M,i,value")
                    # Cela permettra au reducer de faire correspondre avec les éléments de N ayant le même j
                    print(f"{col}\tM,{row},{value}")
                elif matrix == "N":
                    # Pour chaque élément N(j,k), émettre (j, "N,k,value")
                    print(f"{row}\tN,{col},{value}")
        ```
      - `matmul-two-rounds-reduce1.py` :
        ```python
            #!/usr/bin/env python3
            #matmul_two_rounds_reduce1.py
            import sys
            from collections import defaultdict
            
            current_j = None
            m_values = []  # Paires (i, value) de la matrice M
            n_values = []  # Paires (k, value) de la matrice N
            
            for line in sys.stdin:
                # Analyser la ligne d'entrée
                j, data = line.strip().split('\t')
                
                # Si nous rencontrons une nouvelle clé de jointure, traiter la précédente
                if current_j and current_j != j:
                    # Pour chaque paire d'éléments de M et N ayant le même j,
                    # émettre un produit partiel avec la clé (i,k)
                    for m_i, m_val in m_values:
                        for n_k, n_val in n_values:
                            # La clé pour le deuxième round sera (i,k)
                            # La valeur est le produit partiel M(i,j) * N(j,k)
                            partial_product = float(m_val) * float(n_val)
                            print(f"{m_i},{n_k}\t{partial_product}")
                    
                    # Réinitialiser pour la nouvelle clé de jointure
                    m_values = []
                    n_values = []
                
                current_j = j
                
                # Analyser les données en fonction de la matrice
                parts = data.split(',')
                matrix = parts[0]
                
                if matrix == "M":
                    # Stocker (i, value) de M
                    m_values.append((parts[1], parts[2]))
                elif matrix == "N":
                    # Stocker (k, value) de N
                    n_values.append((parts[1], parts[2]))
            
            if current_j:
                for m_i, m_val in m_values:
                    for n_k, n_val in n_values:
                        partial_product = float(m_val) * float(n_val)
                        print(f"{m_i},{n_k}\t{partial_product}")
        ```
      - **Exécution** :
        ```bash
        hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
        -input input-matmul \
        -output matmul-intermediate \
        -mapper matmul-two-rounds-map1.py \
        -reducer matmul-two-rounds-reduce1.py
        ```

    - **Deuxième Round** : Calculer le produit matriciel.
      - `matmul-two-rounds-map2.py` :
        ```python
        #!/usr/bin/env python3
        # matmul_two_rounds_map2.py
        import sys
        
        # Le deuxième mapper est un simple mapper d'identité
        # Il transmet simplement la sortie du premier reducer
        for line in sys.stdin:
            print(line.strip())
                ```
              - `matmul-two-rounds-reduce2.py` :
                ```python
                #!/usr/bin/env python3
                import sys
                from collections import defaultdict
                result = defaultdict(int)
                for line in sys.stdin:
                    key, value = line.strip().split('\t')
                    result[key] += int(value)
                for key, value in result.items():
                    print(f"{key}\t{value}")
                ```
              - **Exécution** :
                ```bash
                hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
                -input matmul-intermediate \
                -output matmul-final \
                -mapper matmul-two-rounds-map2.py \
                -reducer matmul-two-rounds-reduce2.py
        ```
      - `matmul-two-rounds-reduce2.py` :
        ```python
        #!/usr/bin/env python3
        # matmul_two_rounds_reduce2.py
        import sys
        
        current_key = None
        sum_value = 0
        
        for line in sys.stdin:
            # Analyser la ligne d'entrée
            key, value = line.strip().split('\t')
            value = float(value)
            
            # Si nous rencontrons une nouvelle clé, afficher la somme pour la clé précédente
            if current_key and current_key != key:
                # Analyser la ligne et la colonne de la clé
                i, k = current_key.split(',')
                # Afficher dans le format requis : i,k\tvalue (avec un espacement correct)
                print(f"{i},{k}\t {int(sum_value) if sum_value == int(sum_value) else sum_value}")
                sum_value = 0
            
            current_key = key
            sum_value += value
        
        if current_key:
            i, k = current_key.split(',')
            print(f"{i},{k}\t {int(sum_value) if sum_value == int(sum_value) else sum_value}")
        ```
      - **Exécution** :
        ```bash
        hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
        -input matmul-intermediate \
        -output matmul-final \
        -mapper matmul-two-rounds-map2.py \
        -reducer matmul-two-rounds-reduce2.py
        ```
      - **Exécution avec un script `.sh`** :  
      Vous pouvez également exécuter cette tâche en utilisant un script `.sh`. Avec le fichier `run_matmul_two_rounds.sh` :
      ```bash
      chmod +x *.sh
      ./run_matmul_two_rounds.sh
      ``` 
  
  - **Version avec un seul round MapReduce** :
    L'idée ici était d'optimiser le processus en combinant la génération des produits partiels et leur agrégation dans un même round :
    
    - **Mapper**  (matmul-single-round-map.py): Prépare les données en émettant des paires clé-valeur basées sur les indices partagés entre M et N.
    - **Reducer**  (matmul-single-round-reduce.py): Calcule directement les produits partiels et les agrège pour chaque cellule cible.
     
  
    - `matmul-single-round-map.py` :
      ```python
      #!/usr/bin/env python3
      #matmul_single_round_map.py
      import sys
        
        for line in sys.stdin:
            # Analyser la ligne d'entrée
            matrix, i, j, value = line.strip().split('|')
            
            if matrix == "M":
                # Pour chaque élément M(i,j), émettre une paire clé-valeur :
                # clé : j (la dimension commune pour la jointure)
                # valeur : M,i,j,value (pour identifier que cela provient de la matrice M)
                print(f"{j}\tM,{i},{j},{value}")
            elif matrix == "N":
                # Pour chaque élément N(j,k), émettre une paire clé-valeur :
                # clé : j (la dimension commune pour la jointure)
                # valeur : N,j,k,value (pour identifier que cela provient de la matrice N)
                print(f"{i}\tN,{i},{j},{value}")
      ```
    - `matmul-single-round-reduce.py` :
      ```python
         #!/usr/bin/env python3
        #matmul_single_round_reduce.py
        import sys
        from collections import defaultdict
        
        # Dictionnaire pour collecter les produits partiels
        result = defaultdict(float)
        
        current_j = None
        m_elements = []  # Stocker les éléments de M
        n_elements = []  # Stocker les éléments de N
        
        for line in sys.stdin:
            # Analyser la ligne d'entrée
            j, data = line.strip().split('\t')
            
            # Si nous rencontrons une nouvelle clé de jointure, traiter le lot précédent
            if current_j and current_j != j:
                # Pour chaque paire d'éléments de M et N partageant le même j,
                # calculer le produit partiel et l'ajouter au résultat
                for m_data in m_elements:
                    m_parts = m_data.split(',')
                    m_i = m_parts[1]
                    m_value = float(m_parts[3])
                    
                    for n_data in n_elements:
                        n_parts = n_data.split(',')
                        n_k = n_parts[2]
                        n_value = float(n_parts[3])
                        
                        # Ajouter le produit partiel au résultat pour la cellule (i,k)
                        result[(m_i, n_k)] += m_value * n_value
                
                # Réinitialiser pour la nouvelle clé de jointure
                m_elements = []
                n_elements = []
            
            current_j = j
            
            # Analyser et stocker les données en fonction de la matrice
            parts = data.split(',')
            matrix = parts[0]
            
            if matrix == "M":
                m_elements.append(data)
            elif matrix == "N":
                n_elements.append(data)
        
        # Traiter le dernier lot
        if current_j:
            for m_data in m_elements:
                m_parts = m_data.split(',')
                m_i = m_parts[1]
                m_value = float(m_parts[3])
                
                for n_data in n_elements:
                    n_parts = n_data.split(',')
                    n_k = n_parts[2]
                    n_value = float(n_parts[3])
                    
                    # Ajouter le produit partiel au résultat pour la cellule (i,k)
                    result[(m_i, n_k)] += m_value * n_value
        
        # Afficher le résultat final dans le format requis
        for (i, k), value in sorted(result.items()):
            # Convertir en entier si c'est un nombre entier
            formatted_value = int(value) if value == int(value) else value
            print(f"{i},{k}\t {formatted_value}")
      ```
    - **Exécution** :
      ```bash
      hadoop-2.9.1/bin/hadoop jar hadoop-2.9.1/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar \
      -input input-matmul \
      -output matmul-single-round \
      -mapper matmul-single-round-map.py \
      -reducer matmul-single-round-reduce.py
      ```
    - **Exécution avec un script `.sh`** :  
      Vous pouvez également exécuter cette tâche en utilisant un script `.sh`. Avec le fichier `run_matmul_single_round.sh` :
      ```bash
      chmod +x *.sh
      ./run_matmul_single_round.sh
      ``` 


  - **Décisions techniques et justifications:** :
    L'idée ici était d'optimiser le processus en combinant la génération des produits partiels et leur agrégation dans un même round :
    
    - **Utilisation de defaultdict dans les reducers**  Simplifie le stockage et l'accumulation des produits partiels sans avoir à vérifier l'existence des clés.
    - **Gestion des clés dans les mappers**  Le choix des clés (j, "M,i,value") et (j, "N,k,value") permet une jointure efficace des éléments partagés.
    - **Optimisation du tri et des agrégations**  Les reduceByKey sont utilisés au lieu de groupByKey pour réduire le volume des données transférées en réseau.
    - **Contrôle du format de sortie**  Conversion conditionnelle des flottants en entiers pour assurer que la sortie soit conforme à expected-output-matmul.txt.
---

### 2. Spark
- **Objectif** : Réaliser les mêmes tâches (Word Count, Agrégats sur Twitter, Produit matriciel) en utilisant Spark.
- #### 1.1 Installer Java (requis par Spark) :
  Spark nécessite Java pour fonctionner. Nous allons installer OpenJDK, une version libre et open-source de Java.


  ```python
    sudo apt update
    sudo apt install openjdk-11-jdk
    source myenv/bin/activate
    ```

- #### 1.2. Installer Apache Spark :
  Aller sur la page de téléchargement d'Apache Spark : https://spark.apache.org/downloads.html.  
  Sélectionner la version la plus récente (par exemple, Spark 3.5.5).
  
  ```bash
    sudo mv spark-3.5.5-bin-hadoop3.tgz /opt
  ```
  Extraire le fichier :

  ```bash
    cd /opt
    sudo tar -xvzf spark-3.5.5-bin-hadoop3.tgz
  ```
- #### 1.3. Configurer les variables d'environnement  :
  Modifier le fichier .bashrc :

  ```bash
    nano ~/.bashrc
  ```

  Ajouter les lignes suivantes à la fin du fichier :
    
  ```bash
    export SPARK_HOME=/opt/spark-3.5.5-bin-hadoop3
    export PATH=$PATH:$SPARK_HOME/bin
    export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
    export PYSPARK_PYTHON=python
  ```
  Enregistrer et fermer le fichier, puis recharger .bashrc :

  ```bash
   source ~/.bashrc
  ```

  Vérifier l'installation de Spark :

  ```bash
   spark-shell --version
  ```
- #### 1.4.  Installer PySpark :

  Installer PySpark avec pip :

  ```bash
   sudo pip3 install pyspark
  ```
- #### 1.5. Comment exécuter un script avec spark-submit :
  
  Le format général pour exécuter un script avec spark-submit est :

  ```bash
   spark-submit <script.py> <param1> <param2> ... <paramN>
  ```

#### 2.1 Word Count avec Spark
- **Script** : `word-count-spark.py`

- **Exécution** :
  ```bash
  spark-submit word-count-spark.py input-word-count
  ```

#### 2.2 Agrégats sur Twitter avec Spark
- **Script** : `twitter_analysis_spark.py`

- **Exécution** :
  ```bash
  spark-submit twitter_analysis_spark.py social_network.edgelist 

  ```

#### 2.3 Produit matriciel avec Spark
- **Script** : `matmul-spark.py`
  
- **Exécution** :
  ```bash
  spark-submit matmul-spark.py input-matmul output-matmul-spark

  ```
- **Exécution des scripts Spark**

Si vous le souhaitez, vous pouvez exécuter le script `run_scripts.sh` pour obtenir les résultats des trois exercices réalisés avec Spark. Les résultats seront enregistrés dans les dossiers suivants :

- **Word Count** : `spark-output-word-count`
- **Analyse Twitter** : `output/twitter-aggregates.txt`
- **Produit Matriciel** : `output-matmul-spark`

- Commande d'exécution

Utilisez la commande suivante pour exécuter le script :

```bash
chmod +x run_scripts.sh
./run_scripts.sh
```
## Exécution de tous les scripts

Pour exécuter tous les scripts réalisés, vous pouvez utiliser le fichier `run_all.sh`. Avant de l'exécuter, assurez-vous de définir la variable d'environnement `JAVA_HOME`. Voici les commandes à utiliser :

```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
chmod +x *.sh
./run_all.sh
```
---

### 3. Conclusion
Ce projet a permis de mettre en œuvre des tâches de traitement de données massives en utilisant les paradigmes MapReduce et Spark. Les résultats obtenus sont conformes aux attentes et démontrent l'efficacité de ces outils pour le traitement distribué de grandes quantités de données.



---



