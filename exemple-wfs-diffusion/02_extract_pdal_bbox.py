import argparse
import sys
import json

def parse_args():
    parser = argparse.ArgumentParser("Script description")

    # Bounding box de la commune
    # parser.add_argument("--xmin",help="xmin",default=718810,type=float)
    # parser.add_argument("--ymin",help="ymin",default=6693242,type=float)
    # parser.add_argument("--xmax",help="xmax",default=723711,type=float)
    # parser.add_argument("--ymax",help="ymax",default=6699295,type=float)

    # Bounding box d'une zone d'étude plus restreinte
    parser.add_argument("--xmin",help="xmin",default=720000,type=float)
    parser.add_argument("--ymin",help="ymin",default=6697000,type=float)   
    parser.add_argument("--xmax",help="xmax",default=720500,type=float)
    parser.add_argument("--ymax",help="ymax",default=6697500,type=float)
    
    parser.add_argument("--pipeline",help="pipeline",default="pipeline_bbox.json",type=str)
    parser.add_argument("--output",help="output",default="extract_bbox.copc.laz",type=str)
    return parser.parse_args()

def main():
    
    # Parse args
    args = parse_args()
    xmin = args.xmin
    ymin = args.ymin
    xmax = args.xmax
    ymax = args.ymax

    bounds = ([xmin, xmax], [ymin, ymax])
    content = []

    for url in open("dalles_urls.txt").readlines():
        url = url.strip()
        tile = {}
        tile["type"] = "readers.copc"
        tile["filename"] = url
        tile["bounds"] = str(bounds)
        content.append(tile)

    filter = {}
    filter["type"] = "filters.merge"
    content.append(filter)

    writer = {}
    writer["type"] = "writers.copc"
    writer["filename"] = args.output
    content.append(writer)

    pipeline = json.dumps(content, indent=2)
    
    with open(args.pipeline, "w") as f:
        f.write(pipeline)

if __name__ == '__main__':
    sys.exit(main())
