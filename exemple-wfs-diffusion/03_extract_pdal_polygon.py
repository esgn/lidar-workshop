import argparse
import sys
import json
import fiona
from shapely.geometry import shape

def parse_args():
    parser = argparse.ArgumentParser("Script description")
    parser.add_argument("--polygon",help="polygon",default="menou.gpkg",type=str)
    parser.add_argument("--pipeline",help="pipeline",default="pipeline_polygon.json",type=str)
    parser.add_argument("--output",help="output",default="extract_polygon.copc.laz",type=str)
    return parser.parse_args()

def main():
    # Parse args
    args = parse_args()

    # Read polygon (force simple polygon here)
    wkt_value = None
    with fiona.open(args.polygon) as src:
        feature = next(iter(src))
        geom = shape(feature["geometry"])
        polygon = list(geom.geoms)[0] 
        wkt_value = polygon.wkt

    content = []

    for url in open("dalles_urls.txt").readlines():
        url = url.strip()
        tile = {}
        tile["type"] = "readers.copc"
        tile["filename"] = url
        tile["polygon" ] = wkt_value
        content.append(tile)

    filter = {}
    filter["type"] = "filters.merge"
    content.append(filter)

    writer = {}
    writer["type"] = "writers.copc"
    # writer["forward"] = "all"
    # writer["extra_dims"] = "all"
    # writer["a_srs"] = "EPSG:2154"
    writer["filename"] = args.output
    content.append(writer)

    pipeline = json.dumps(content, indent=2)
    with open(args.pipeline, "w") as f:
        f.write(pipeline)

if __name__ == '__main__':
    sys.exit(main())
