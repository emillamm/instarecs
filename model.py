#!/usr/bin/env python

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
    "Column('id', Integer, Sequence('user_id_seq'), primary_key=True),"
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


