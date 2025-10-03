# Exemple PDAL et diffusion LIDAR HD

On s'intéresse dans cette partie à la commune de Menou (58210), dont le contour est fourni par le fichier `menou.gpkg`.


## Création d'un environnement conda

```bash
conda create -c conda-forge -n pdal-workshop pdal pdal_wrench gdal fiona
conda activate pdal-workshop
```


## Télécharger la liste des dalles correspondant à la zone d'intérêt

On utilise le script `01_get_dalles.py`. Il est possible de passer la zone d'intérêt en paramètre. Pour cette première utilisation on se contentera des paramètres par défaut qui correspondent à la commune de Menou.

Ce script utilise un flux WFS de la Géoplateforme pour permettre la récupération des dalles sur une zone d'intérêt.

```bash
python3 01_get_dalles.py
```

Deux fichiers sont produits :
* `dalles.gpkg` qui contient les géométries et attributs des dalles récupérs depuis le WFS. Ce fichier n'est utile que pour visualiser la zone.
* `dalles_urls.txt` qui contient la liste des URLs des dalles qui va nous servir par la suite.


## Extraction d'une portion de la zone d'intérêt au format COPC avec PDAL

On utilise pour cela le script `02_extract_pdal_bbox.py` qui génère la pipeline PDAL nécessaire à l'extraction de la zone à partir de la liste des URLs des dalles. On utilise une zone d'intérêt réduite pour éviter un traitement trop long.

```bash
python3 02_extract_pdal_bbox.py
```

Ce script génère un fichier `pipeline_bbox.json`. On éxécute cette pipeline via la commande `pdal pipeline pipeline_bbox.json -v 8`.  

Ce traitement prend quelque minutes et aboutit à la création du fichier `extract_bbox.copc.laz`. Un simple drag and drop dans QGIS permet de visualiser ce fichier.


## Extraction de la zone d'intérêt suivant son contour polygonal

On va cette fois ci extraire la couverture LIDAR HD suivant le contour de la commune de Menou.

Pour ce faire on utilise le script `03_extract_pdal_polygon.py` qui permet d'obtenir une pipeline PDAL `pipeline_polygon.json`.

```bash
python3 03_extract_pdal_polygon.py
```

On éxécute cette pipeline via la commande `pdal pipeline pipeline_polygon.json -v 8`. 

Ce traitement prend **40 minutes** et aboutit à la création du fichier `extract_polygon.copc.laz`. Un simple drag and drop dans QGIS permet de visualiser ce fichier.


## Constitution d'un VPC à partir de la liste des dalles de la zone d'intérêt

On va utiliser cette fois-ci `pdal_wrench` pour générer un VPC correspondant à notre zone d'intérêt à partir de la liste des urls des fichiers.  

```bash
pdal_wrench build_vpc --output menou.vpc --input-file-list=dalles_urls.txt
```

On peut visualiser ce VPC dans QGIS via un simple drag and drop. A noter que les données ne deviennent visibles qu'à partir un certain niveau de zoom.


## Extraction de la zone d'intérêt suivant son contour polygonal via le fichier VPC

On utilise `pdal_wrench` pour découper la zone d'intérêt à l'aide du polygone de la commune.

A la différence de PDAL, `pdal_wrench` ne propose pas d'option permettant de découper et merger les résultats en une seule opération. Il va donc ici nous falloir executer deux opérations différentes sur le vpc.

Première étape consistant à découper le lidar suivant le polygone de la zone d'intérêt

```bash
pdal_wrench clip --input=menou.vpc --polygon=menou.gpkg --output=menou_clipped.vpc --output-format=laz 
```

Cette première étape prend environ **4 minutes**. On tire ici grandement parti des capacités de multi-threading de `pdal_wrench`.

On observe la création d'un dossier `menou_clipped` qui contient tous les morceaux de dalles extraits en laz. Ces éléments sont référencés par un VPC nommé `menou_clipped.vpc`.

On vient ensuite concatener les fichiers obtenus en utilisant la commande suivante :

```bash
pdal_wrench merge --output=menou_merged.copc.laz menou_clipped.vpc
```

Cette deuxième étape prend environ **30 minutes**. `pdal_wrench` est monothreadé sur l'opération de merge et semble globalement moins efficace que PDAL pour cette partie.

