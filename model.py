#!/usr/bin/env python

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import fields
col_string = ""
for i in xrange(4):
    col_string += ("Column('val" + str(i) + "', Numeric, nullable=False), ")

evalstr = ("umat = Table('umat', metadata,"
    "Column('id', Integer, nullable=False, primary_key=True),"
    "Column('uid', Integer, nullable=False),"
    + col_string[:-2]
    + ")"
)

exec(evalstr)
