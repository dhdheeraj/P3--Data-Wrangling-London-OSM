######################### auditing street names ########################
osmfile = "london_sample_post_update.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Avenue", "Boulevard", "Court","Drive", "Lane", "Place", "Parkway",   "Road", "Route", "Street", 
            "Square", "Trail", "Way"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])####### audidting street names by creating sets of all street types in data set####
    osm_file.close()
    return street_types

st_types=audit(osmfile)
pprint.pprint(dict(st_types))
#### cleaning######
###################cleaning street names#######################
import pprint
mapping = {
        
        'Rd': 'Road',
        'Ridgway': 'Ridgeway',
        'Rioad':'Road',
        'Sq': 'Square',
        'St':'Street',
        'St.':'Street',
        'Ave':'Avenue',
        'street':'Street',
        'Way)':'Way'
        }


all_street_word = set()
name_list = []

def clean_street(osmfile):
    osm_file = open(osmfile, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag in["node", "way", "relation"] :
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    better_name = update_name(tag.attrib['v'])
                    name_list.append(better_name)
                    
    osm_file.close()
    return name_list

def update_name(name):
    
   
    if (re.findall(r".*",name)):     ###########using regex to find street names with commas#####
        
        name= name.split(",")[0].strip() ##########splitting near comma and taking first name######
        if (re.findall(r"'(.*?)'", name)): ######## extracting street names in single quotes if present in first part###
            
            name= str(re.findall(r"'(.*?)'", name, re.DOTALL)) ######converting extracted part from list to string###
            for char in string.punctuation:               ######removing symbols#####
                name=name.replace(char,'')                
        
    for n in name.split():
        if n in mapping:                              ###### if any part of the street name present in mapping, it is replaced with the full form as specified in mapping###
            name = name.replace(n, mapping[n])
        if n=='The':
            name=name.replace(" ","")
            name= name.replace(n,'')
        
    
    return name



st_name = clean_street('london_sample_post_update.osm')
pprint.pprint(st_name)
#### writing osm#####
def writer(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    tree = ET.parse(osmfile)
    listtree = list(tree.iter())
    for elem in listtree:

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    old = tag.attrib['v'] 
                    new = update_name(tag.attrib['v']) ####writer function updates new names along with old ones####
                    if old != new:
                        
                        tag.attrib['v'] = new
                        tag.set('updated', 'yes')
    
    tree.write('london_sample_final.osm')
    osm_file.close()
    return street_types
writer('london_sample_post_update.osm')