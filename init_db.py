#!/usr/bin/env python
import json
from sqlalchemy import *
import fields

conn_string = fields.dbtype + '://' + fields.dbuser + ':' +  fields.dbpass + '@' + fields.dbhost + '/' + fields.dbname;
engine = create_engine(conn_string)

connection = engine.connect()

metadata = MetaData()

col_string = ""
for i in xrange(fields.K):
    col_string += ("Column('val" + str(i) + "', Numeric, nullable=False), ")

evalstr = ("umat = Table('umat', metadata,"
    "Column('id', Integer, nullable=False, primary_key=True),"
    "Column('uid', Integer, nullable=False),"
    + col_string[:-2]
    + ")"
)
exec(evalstr)

evalstr = ("vmat = Table('vmat', metadata,"
    "Column('id', Integer, nullable=False, primary_key=True),"
    "Column('vid', Integer, nullable=False),"
    + col_string[:-2]
    + ")"
)
exec(evalstr)

metadata.drop_all(engine)
metadata.create_all(engine)

#Insert items into table
#for row in json_object:
    #ins = item_store.insert().values(id=row['id'], title=row['title'], year=row['year'], count=row['count'], rating=row['rating']) 
    #connection.execute(ins)

