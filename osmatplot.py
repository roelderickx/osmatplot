#!/usr/bin/python

import sys, argparse, logging
from xml.dom import minidom
import matplotlib.pyplot as pyplot

logging.basicConfig(level = logging.INFO)

parser = argparse.ArgumentParser(description='Rough visualization of an OSM file with matplotlib')
parser.add_argument("input", metavar="OSMFILE", help="Input osm file")
args = parser.parse_args()

#xmldoc = minidom.parse("nightingale_island.osm")
xmldoc = minidom.parse(args.input)
xmlosmnode = xmldoc.getElementsByTagName('osm')[0]

# reading data
logging.info("Reading nodes")
count = 0
nodes = {}
for nodenode in xmlosmnode.getElementsByTagName('node'):
    identif = int(nodenode.attributes['id'].value)
    nodes[identif] = (float(nodenode.attributes['lon'].value),
                      float(nodenode.attributes['lat'].value),
                      False)
    count += 1
logging.info("%d nodes found" % count)

logging.info("Reading ways")
count = 0
ways = []
for waynode in xmlosmnode.getElementsByTagName('way'):
    identif = int(waynode.attributes['id'].value)
    way_nodes = []
    for waynodenode in waynode.getElementsByTagName('nd'):
        nd_identif = int(waynodenode.attributes['ref'].value)
        way_nodes.append(nd_identif)
    ways.append(way_nodes)
    count += 1
logging.info("%d ways found" % count)

# rendering data
pyplot.title(args.input)

logging.info("Rendering ways")
for way in ways:
    way_x = []
    way_y = []
    for node in way:
        (x, y, is_rendered) = nodes[node]
        if not is_rendered:
            nodes[node] = (x, y, True)
        way_x.append(x)
        way_y.append(y)
    pyplot.plot(way_x, way_y)

logging.info("Rendering additional nodes")
for (x, y, is_rendered) in [ node for node in nodes.values() if not node[2] ]:
    pyplot.plot(x, y, '+')

pyplot.show()

