# Exemple entwine

Exemple simple de colorisation d'une dalle LIDAR HD et diffusion en EPT

## Création d'un environnement conda

```bash
conda create -c conda-forge -n entwine-workshop entwine pdal
conda activate entwine-workshop
```

## Télécharger une dalle de LIDAR HD

```bash
wget "https://storage.sbg.cloud.ovh.net/v1/AUTH_63234f509d6048bca3c9fd7928720ca1/ppk-lidar/LH/LHD_FXX_0721_6697_PTS_C_LAMB93_IGN69.copc.laz"
```

## Récupérer la bounding box de la dalle

On passe par pdal info pour récupérer les informations concernant la dalle LIDAR HD téléchargée

```bash
pdal info LHD_FXX_0721_6697_PTS_C_LAMB93_IGN69.copc.laz
```

```json
     "native":
      {
        "bbox":
        {
          "maxx": 722000,
          "maxy": 6697000,
          "maxz": 328.63,
          "minx": 721000,
          "miny": 6696000,
          "minz": 261.48
        },
```

La bounding box des données est donc : `721000,6696000,722000,6697000`

## Récupérer la dalle d'orthophotographie IGN pour coloriser le LIDAR HD

On fait une requête WMS pour récupérer la dalle d'ortho correpondant à la bounding box

```bash
wget -O dalle.tif "https://data.geopf.fr/wms-r?request=GetMap&service=WMS&version=1.3.0&BBOX=721000,6696000,722000,6697000&LAYERS=ORTHOIMAGERY.ORTHOPHOTOS&WIDTH=4000&HEIGHT=4000&CRS=EPSG:2154&STYLES=&FORMAT=image/geotiff"
```

## Colorisation de la dalle LIDAR HD

On passe cette fois-ci par une pipeline PDAL pour coloriser la dalle LIDAR HD

```json
[
    "LHD_FXX_0721_6697_PTS_C_LAMB93_IGN69.copc.laz",
    {
        "type": "filters.colorization",
        "raster": "dalle.tif"
    },
    "LHD_FXX_0721_6697_PTS_C_LAMB93_IGN69-COLOR.copc.laz"
]
```

On joue cette pipeline en sauvegardant ce contenu dans un fichier `pipeline.json` et en la lancant avec `pdal pipeline pipeline.json -v 8`

## Visualisation de la dalle colorisée dans QGIS

On drag and drop le fichier `LHD_FXX_0721_6697_PTS_C_LAMB93_IGN69-COLOR.copc.laz` dans QGIS.


## Création d'un EPT avec entwine

On créé le dossier de sortie et on lance la commande entwine qui va créer l'EPT

```bash
mkdir EPT
entwine build -i LHD_FXX_0721_6697_PTS_C_LAMB93_IGN69-COLOR.copc.laz -t $(nproc) -o EPT/
```

## Visualisation de l'EPT dans QGIS

On drag and drop simplement le fichier `EPT/ept.json` dans QGIS


## Visualisation via le viewer Potree

On installe nodejs pour installer le paquet npm http-server

```bash
conda install -c conda-forge nodejs -y
npm install http-server -g
http-server -p 8080 --cors
```

On peut visualiser l'EPT via le viewer Potree à l'URL `https://potree.entwine.io/data/view.html?r="http://localhost:8080/EPT/"`


## Utilisation de l'EPT comme source de données pour PDAL

Exemple 

```bash
pdal translate ept://EPT menou.tif --writers.gdal.resolution=0.5 --writers.gdal.dimension=Z --writers.gdal.output_type=max
gdaldem hillshade menou.tif hillshade.png
```
