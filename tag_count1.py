############### getting tag counts#################3
import xml.etree.cElementTree as ET
from collections import defaultdict

import pprint
tag_types = defaultdict(int)
def count_tags(filename):
    
    mytags =  defaultdict(int)
    osmfile = open(filename, 'r')
    for event, child in ET.iterparse(filename):
        if child.tag in mytags:                 ###########creating default dictionaries for tags and appending them by 1 every time a new tag is found
            mytags[child.tag] += 1              ###########
        else:
            mytags[child.tag] = 1
    return mytags
   

tags = count_tags('london_sample.osm')
pprint.pprint(tags)