import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "london_sample_final.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def correct_k(k):
    index=k.find(':')
    typ=k[:index]
    k=k[index+1:]    
    return k,typ

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    
    
    if element.tag=='node':            ########node attributes handling#####
        try:
            
            for i in node_attr_fields:
            
                if i=='id' or i=='uid' or i=='changeset' and element.attrib[i]:
                    node_attribs[i] = int (element.attrib[i])
                    
                elif i == 'lat' or i == 'lon' and element.attrib[i]:
                    node_attribs[i] = float (element.attrib[i])
                    
                elif i == 'user' and element.attrib[i]:
                    node_attribs[i] = str(element.attrib[i].encode('ascii', 'ignore').decode('ascii'))
                    
                else:
                    node_attribs[i] = element.attrib[i]
        except KeyError:
            return None       ##########if tags do not have all attributes the whole element is not considered for further analysis###
           
            
    if element.tag=='way':
        for i in way_attr_fields:
            way_attribs[i]=element.attrib[i]    ##### way atrributes handling#########
        
    for tag in element.iter("tag"):
        dic={}
        attributes=tag.attrib
        if problem_chars.search(tag.attrib['k']):     ####proble character attributes avoided####
            continue
        
        if element.tag=='node':
            dic['id']=node_attribs['id']
        else:
            dic['id']=way_attribs['id']
        
        dic['value'] = attributes['v']

        colon_k=LOWER_COLON.search(tag.attrib['k'])    ####lower colon attributes split####
        if colon_k:
            print colon_k.group(0)
            print tag.attrib['k']
            dic['key'],dic['type']=correct_k(tag.attrib['k'])
        else:
            dic['key']=attributes['k']
            dic['type']='regular'
        
        
        #print dic
        tags.append(dic)
    
    if element.tag=='way':
        position=0
        for nd in element.iter("nd"):
            way_node_dic={}
            way_node_dic['id']=way_attribs['id']              ##########way node atrributes handling##########
            way_node_dic['node_id']=nd.attrib['ref']
            way_node_dic['position']=position
            position = position + 1
            way_nodes.append(way_node_dic)
             
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags :
            yield elem
            #print elem
            #print elem.attrib['user']
            root.clear()


def validate_element(element, validator, schema=SCHEMA):

        
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))       #########validating schema####
    
        
        
        


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)