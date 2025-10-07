import os
import sys
import glob
import argparse

try:
    from osgeo import ogr, osr, gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')


def parse_args():
    parser = argparse.ArgumentParser("Script description")
    parser.add_argument("--xmin", help="xmin", default=718810, type=float)
    parser.add_argument("--ymin", help="ymin", default=6693242, type=float)
    parser.add_argument("--xmax", help="xmax", default=723711, type=float)
    parser.add_argument("--ymax", help="ymax", default=6699295, type=float)
    parser.add_argument("--ftype", help="feature type",
                        default="IGNF_NUAGES-DE-POINTS-LIDAR-HD:dalle", type=str)
    parser.add_argument("--output", help="output",
                        default="dalles.gpkg", type=str)
    return parser.parse_args()


def main():

    # Parse args
    args = parse_args()
    xmin = args.xmin
    ymin = args.ymin
    xmax = args.xmax
    ymax = args.ymax

    # create the spatial reference
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(2154)

    # Set the driver (optional)
    wfs_drv = ogr.GetDriverByName('WFS')

    # Speeds up querying WFS capabilities for services with alot of layers
    gdal.SetConfigOption('OGR_WFS_LOAD_MULTIPLE_LAYER_DEFN', 'NO')

    # Set config for paging. Works on WFS 2.0 services and WFS 1.0 and 1.1 with some other services.
    gdal.SetConfigOption('OGR_WFS_PAGING_ALLOWED', 'YES')
    gdal.SetConfigOption('OGR_WFS_PAGE_SIZE', '5000')

    # Open the webservice
    # Get features in EPSG:2154 with only the cleabs attribute
    url = 'https://data.geopf.fr/wfs?SERVICE=WFS&SRSNAME=EPSG:2154'
    wfs_ds = wfs_drv.Open('WFS:' + url)
    if not wfs_ds:
        sys.exit('ERROR: cannot open WFS datasource')
    else:
        pass

    # Get a specific feature type
    layer = wfs_ds.GetLayerByName(args.ftype)
    wkt = f"POLYGON (({xmin} {ymin},{xmax} {ymin},{xmax} {ymax},{xmin} {ymax},{xmin} {ymin}))"
    geometry = ogr.CreateGeometryFromWkt(wkt, srs)
    layer.SetSpatialFilter(geometry)

    # Write to gpkg
    dr = ogr.GetDriverByName('GPKG')
    ds = dr.CreateDataSource(args.output)
    ds.CopyLayer(layer, 'dalles')

    # Export features url column to txt file
    with open('dalles_urls.txt', 'w') as f:
        for feat in layer:
            url = feat.GetField('url')
            if "data.geopf.fr/telechargement" in url:
                url.replace("data.geopf.fr/telechargement",
                            "data.geopf.fr/chunk/telechargement")
            f.write(url + '\n')

    return 0


if __name__ == '__main__':
    sys.exit(main())
