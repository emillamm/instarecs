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

#Get list of column names
col_names = []
first_row = json_object[0]
for key in first_row:
    col_names.append(key)

#Create new database
q = ("DROP TABLE IF EXISTS item_store;"
                "CREATE TABLE item_store ("
                    "id INTEGER NOT NULL PRIMARY KEY,"
                    "title TEXT NOT NULL," + 
                    "year  INTEGER NOT NULL," +
                    "count INTEGER NOT NULL," +
                    "rating NUMERIC NOT NULL" +
                ");")
engine.execute(q)


#Insert items into table
for row in json_object:
    q = ("INSERT INTO item_store (id, title, year, count, rating) "
            "VALUES ( %i, %s, %i, %i, %d );" )
    values = (str(row['id']) + ", '" + 
            row['title'].encode("ISO-8859-1") + "'," + 
            str(row['year']) + "," + 
            str(row['count']) + "," + 
            str(row['rating']) )
    engine.execute(q,values)


