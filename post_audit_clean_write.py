####### postal code audit#######
def is_postalcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def post_audit(osmfile):
    osm_file = open(osmfile, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postalcode(tag):
                    pin=str(tag.attrib['v']) #### converting codes as strings and viewing####
                    print pin
                    
                    
                   
                   
    osm_file.close()
post_audit('london_sample_phone_update.osm')
######cleaning#####
import string
def post_clean(code):

    
    old=code
    if len(code) < 6:        #########excluding codes less than 6 or 8 characters including the whitespace#####
        new='None'
    if len(code) > 8:
        new='None'
    if len(code)>= 6 and len(code)<= 8: 
        m= code.split(' ')
        pre=m[0]
        post=m[1]                            ###############splitting the code to generate pre and post code######
        if pre[0] == 'Q' or pre[0]=='V' or pre[0]=='X':
            new='None'                         ###########evaluating pre code, if meeting specification labelled as none######
        if pre[1]=='I' or pre[1]=='J' or pre[1]=='Z':
            new='None'
        if post[0] not in string.digits:        ####### evaluating post code, if meeting specification labelled as none###
            new='None'
        else:
            new=old                       ##### if in proper format code remains as is#####
    
        
    print old,'=>',new
    return new
####writing####
def writer_post(osmfile):
    osm_file = open(osmfile, "r")
    tree = ET.parse(osmfile)
    listtree = list(tree.iter())
    for elem in listtree:

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postalcode(tag):
                    old = str(tag.attrib['v'])
                    new = post_clean(str(tag.attrib['v']))
                    if (new == 'None'):
                        elem.remove(tag)
                    else:
                        tag.attrib['v'] = new                #######writer function removes the post codes returned as none from cleaning#######
                        tag.set('updated', 'yes')
                        
                        
                            
                        
                        
                        
    tree.write('london_sample_post_update.osm')
    
    osm_file.close()
writer_post('london_sample_phone_update.osm')