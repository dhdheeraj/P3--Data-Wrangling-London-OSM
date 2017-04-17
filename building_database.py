##### creating database#####
"""
Build database of the CSV files with the repective table names.
"""

import csv, sqlite3

con = sqlite3.connect("london.db")
con.text_factory = str
cursor = con.cursor()

# create nodes table
cursor.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp);")
with open('nodes.csv','rb') as fin:
    loop = csv.DictReader(fin) 
    lbase = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) \
             for i in loop]

cursor.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);", lbase)
con.commit()

#create nodes_tags table
cursor.execute("CREATE TABLE nodes_tags (id, key, value, type);")
with open('nodes_tags.csv','rb') as fin:
    loop = csv.DictReader(fin) 
    lbase = [(i['id'], i['key'], i['value'], i['type']) for i in loop]

cursor.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", lbase)
con.commit()

#Create ways table
cursor.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")
with open('ways.csv','rb') as fin:
    loop = csv.DictReader(fin) 
    lbase = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in loop]

cursor.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", lbase)
con.commit()

#Create ways_nodes table
cursor.execute("CREATE TABLE ways_nodes (id, node_id, position);")
with open('ways_nodes.csv','rb') as fin:
    loop = csv.DictReader(fin) 
    lbase = [(i['id'], i['node_id'], i['position']) for i in loop]

cursor.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", lbase)
con.commit()

#Create ways_tags table
cursor.execute("CREATE TABLE ways_tags (id, key, value, type);")
with open('ways_tags.csv','rb') as fin:
    loop = csv.DictReader(fin) 
    lbase = [(i['id'], i['key'], i['value'], i['type']) for i in loop]

cursor.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", lbase)
con.commit()