#!/usr/bin/env python
import json
from sqlalchemy import *
import fields
import random
from model import *



metadata.drop_all(engine)
metadata.create_all(engine)

s = text("SELECT " + fields.itemtable + ".id FROM " + fields.itemtable)
result = connection.execute(s).fetchall()
for row in result:
    vid = row[0]
    #insstr = (id=1, uid=1, val1=1, val2=1)
    #ins = vmat.insert().values(insstr)
    insstr = "vid=" + str(vid) + ","
    rand = [random.random() for i in xrange(fields.K)]
    for i in xrange(fields.K):
        insstr += ("val" + str(i) + "=" + str(rand[i]) + ",")
    insstr_eval = "ins = vmat.insert().values(" + insstr[:-2] + ")"
    exec(insstr_eval)
    connection.execute(ins)

#Insert items into table
#for row in json_object:
    #ins = item_store.insert().values(id=row['id'], title=row['title'], year=row['year'], count=row['count'], rating=row['rating']) 
    #connection.execute(ins)

