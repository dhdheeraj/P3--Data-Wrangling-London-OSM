import os
def file_size(filename):
    print filename, "------", float(os.path.getsize(filename))/(1024*1024), "MB"
file_size('london_england.osm')
file_size('london_sample_final.osm')
file_size('london.db')
file_size('nodes.csv')
file_size('ways.csv')
file_size('nodes_tags.csv')
file_size('ways_tags.csv')
file_size('ways_nodes.csv')