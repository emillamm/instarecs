#!/usr/bin/env python
import json
from sqlalchemy import *
import fields

json_data = open('movies.json','r')
json_object = json.load(json_data)
conn_string = fields.dbtype + '://' + fields.dbuser + ':' +  fields.dbpass + '@' + fields.dbhost + '/' + fields.dbname;
engine = create_engine(conn_string)

connection = engine.connect()
q = "select version();"
result = engine.execute(q)
row = result.fetchone()
print(row[0])
a = 0

#Insert items into table
for row in json_object:
    ins = item_store.insert().values(id=row['id'], title=row['title'], year=row['year'], count=row['count'], rating=row['rating']) 
    connection.execute(ins)

