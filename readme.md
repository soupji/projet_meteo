# Projet météo: API Open Weather

Le but de se projet est de requêter l'API Open Weather afin de faire des analyses statistiques sur les villes françaises. 

Au-delà de manipuler des libraires de datavisualisation, le but du projet était aussi de pouvoir manipuler différentes technologies au sein d'un même projet, notamment docker et mongodb.

### Technologies utilisées
- python
- flask
- docker
- mongodb

### Fonctionnalités principales
- Récupèrer les JSON exposée par l'API via une route flask en utilisant en paramètre l'id de la ville
- Sauvegarder les données relatives aux villes françaises dans une base mongodb
- Le projet est fonctionnel via docker et la conteneurisation

### Architecture projet
``` bash
|- projet meteo
|   |- python
|       |- main.py: code python principal du projet
|       |- projet_meteo.ipynb: jupyter notebook pour la datavisuliation
|       |- requirements.txt: libraires nécessaires à installer (gérer automatiquement via docker)
|       |- dockerfile: fichier docker, image python
|   |- mongodb
|       |- base_mongodb.js: fichier générique pour la création de la base + collection mongodb
|       |- dockerfile: fichier docker, image mongodb
|   |- templates
|       |- data.html: homepage flask
|   |- docker-compose.yml: docker compose pour la gestion des conteneurs
|   |- readme.md: readme pour le projet
|   |- screenshot_run_projet_local.pdf: différents screens pour montrer les résultats du projet en local
```

![Schéma d'architecture du projet](https://github.com/soupji/projet_meteo/blob/master/schema_architecture.png?raw=true)

### Routes flask
``` bash
- localhost:5000/: home page générale
- localhost:5000/weather/<city_id>: récupérer les JSON pour une ville donnée (id de la ville)
- exemple: localhost:5000/weather/2968815
```

## Guide d'utilisation

### Prérequis
- Avoir l'interpreteur python et docker desktop.
- Le port d'écoute pour la base mongodb utilisé tout au long du projet est le **27017**.

### Note sur le Jupyter Notebook
Les analyses de datavisualisation ont été générés avec Jupyter Notebook, sur ~30 000 lignes de données, sur la journée du 31 décembre.  
  
Il est tout à fait possible de relancer le Jupyter, avec des données plus récentes. Attention à installer les librairies nécessaires au préalable, car il n'y a pas de pip install dans le notebook.
``` bash
/!\ La dockerisation du projet ne comprend pas le Jupyter Notebook, donc la connexion à la base mongodb se fait en local.
```

### Run du projet
- Télécharger l'archive du projet git
- Lancer un invite de commandes:

    - Sans passer par docker:
        ``` bash
        - cd 'projet meteo/python/'
        - python main.py
        ```
        - Sauvegarder les données dans une base mongodb **(y/n)?:**
            - **y:** Le code tourne jusqu'à une interruption manuel (ctrl c)
            - **n:** Utiliser les routes flask
        ``` bash
        /!\: essayer de sauvegarder les données dans la base mongodb sans passer par docker génèrera une erreur, car les identifiants de connexion sont parametrés pour le docker compose.
        ```

    - Utiliser docker:
        ``` bash
        - cd 'projet meteo'/
        - docker compose up -d (avec le properties adéquates pour gérer le input dans la console)
        ```
        - Deux conteneurs sont par la suite généré au sein du conteneur **projetmeteo:**
            - **projet_meteo_python:** interaction avec le code python
            - **projet_meteo_mongodb:** base mongodb, utilisable en ligne de commande (dans le conteneur) via la commande mongosh
``` bash
/!\: pour sauvegarder les données dans la base mongodb, il faut entrer 'y' dans le conteneur python, puis basculer sur le conteneur mongodb pour voir les lignes nouvellement ajoutées.
```