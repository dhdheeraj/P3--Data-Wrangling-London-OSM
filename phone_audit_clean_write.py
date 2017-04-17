############# final phone audit to go into proj############3
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import string
def is_phone(elem):
    return (elem.attrib['k'] == "phone")

def phone_audit(osmfile):
    osm_file = open(osmfile, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_phone(tag):
                    ph=str(tag.attrib['v'].replace(" ","").encode('ascii', 'ignore').decode('ascii')) ###converting phone numbers to strings###
                    print ph
                    
                   
                   
    osm_file.close()
phone_audit('london_sample.osm')
########### shape function for all phone numbers###########
def phone_clean(number):
    old=number
    if len(number)<=11:                        #####checking numbers less than or equal to 11 digits
        if number[0:3] == '020':
            updated = '+44'+'-'+ number[1:3]+ '-'+ number[3:7]+ '-'+ number[7:11]
        else:
            updated = '+44'+'-'+ number[1:5]+ '-'+ number[5:11]
    if len(number)>11:                         #####cleaning for numbers greater than 11######
        if number[0:3]=="+44":
            for char in string.punctuation:
                number=number.replace(char,'')   ####removing symbols such as '(' ')' from the numbers####
        
        if len(number)>12:                      ###for those which are greater than 12 i.e. numbers with irreleavant codes
            
            if number[2]=='0' and number[3:5]=="20":
                updated='+'+number[0:2]+'-'+number[3:5]+'-'+number[5:9]+'-'+number[9:13]
            elif number[2]=='0' and number[3:5]!="20":
                updated='+'+number[0:2]+'-'+number[3:7]+'-'+number[7:13]
            else:
                updated = 'None'
        else:
            if number[2:4]=="20":                 ######### for entries with more than 1 number, the first number is considered ####
                updated='+'+number[0:2]+'-'+number[2:4]+'-'+number[4:8]+'-'+number[8:12]
            if number[2:4]!="20":
                updated='+'+number[0:2]+'-'+number[2:6]+'-'+number[6:12]
    print old,"=>",updated
    return updated
################# updating osm file #########################
def writer_phone(osmfile):
    osm_file = open(osmfile, "r")
    tree = ET.parse(osmfile)
    listtree = list(tree.iter())
    for elem in listtree:

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_phone(tag):
                    old = str(tag.attrib['v'].replace(" ","").encode('ascii', 'ignore').decode('ascii'))
                    updated = phone_clean(str(tag.attrib['v'].replace(" ","").encode('ascii', 'ignore').decode('ascii')))
                    if (updated == 'None'):
                        elem.remove(tag)
                    else:
                        tag.attrib['v'] = updated    ######## writer function updating the osm file and excluding the tags with none as phonenumber##
                        tag.set('updated', 'yes')
                        #elem.remove(tag)
                        
                            
                        
                        
                        
    tree.write('london_sample_phone_update.osm')
    
    osm_file.close()
writer_phone('london_sample.osm')
   