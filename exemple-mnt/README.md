# Tests génération MNT

## Création d'un environnement conda

```bash
conda create -c conda-forge -n pdal-workshop pdal pdal_wrench gdal fiona
conda activate pdal-workshop
```
## Télécharger une dalle de LIDAR HD

```bash
wget "https://storage.sbg.cloud.ovh.net/v1/AUTH_63234f509d6048bca3c9fd7928720ca1/ppk-lidar/LH/LHD_FXX_0721_6697_PTS_C_LAMB93_IGN69.copc.laz"
```

## Avec PDAL

Lancer la pipeline suivante

```
pdal pipeline pipeline_tin.json -v 8
```

Ouvrir le résultat `output_mnt_tin.tif` dans QGIS et utiliser l'outil `Raster > Analyse > Remplir NoData` pour trianguler les trous du MNT s'il en reste (ne devrait pas arriver. bug pdal?)


## Avec PDAL wrench

```bash
pdal_wrench to_raster_tin --input=LHD_FXX_0721_6697_PTS_C_LAMB93_IGN69.copc.laz --output=OUTPUT.tif --resolution=0.5 --tile-size=1000 "--filter=Classification == 2 || Classification == 66" "--bounds=([721000, 722000], [6696000, 6697000])" --threads=$(nproc)
```
 Ouvrir le résultat dans QGIS pour visualiser le MNT produit




