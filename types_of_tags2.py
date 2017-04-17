########### lower,problem chars ################
import xml.etree.ElementTree as ET
import re
lower = re.compile(r'^([a-z]|_)*$')             ######using regex to finf lower case aphabet
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')          ###########using regex to find lower case alphabet with colon
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')        ########using regex to find problem characters in attributes

lows = set()
lows_colon = set()
probs_chars = set()
others = set()



def key_type(element, keys):
    if element.tag == "tag":
        #print element.attrib['k']
        # YOUR CODE HERE
        if(lower.search(element.attrib['k'])):
            #print "--------lower"
            keys['lower'] += 1                             #####creating dictionary with lower,lower_colon,problem_chars as keys adding element attributes to these keys if they belong to them
            lows.add(element.attrib['k'])
        elif (lower_colon.search(element.attrib['k'])):
            #print "--------lowercolon"
            keys['lower_colon'] += 1
            lows_colon.add(element.attrib['k'])
        elif (problemchars.search(element.attrib['k'])):
            #print "--------problemchars"
            keys['problemchars'] += 1
            probs_chars.add(element.attrib['k'])
        else:
            #print "--------others"
            keys['other'] += 1
            others.add(element.attrib['k'])
    return keys


    
    
        
    



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys
    

process_map('london_sample.osm')
