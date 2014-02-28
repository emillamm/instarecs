#!/usr/bin/env python
import json
from sqlalchemy import *
import fields
import random
from model import *
import numpy as np

def add_user(uid):
    insstr = "uid=" + str(uid) + ","
    rand = [random.random() for i in xrange(3)]
    for i in xrange(fields.K):
        insstr += ("val" + str(i) + "=" + str(rand[i]) + ",")
    insstr_eval = "ins = umat.insert().values(" + insstr[:-2] + ")"
    exec(insstr_eval)
    connection.execute(ins)
    return 0    

def update_choice(vid1, vid2, uid):
    a = fields.alpha
    l = fields.lambd
    pc = 1

    s = select([umat]).where(umat.c.uid == uid)
    result = connection.execute(s).fetchone()
    result_list  = [r for r in result][2:]
    u =  np.array(result_list)

    s = select([vmat]).where(vmat.c.vid == vid1)
    result = connection.execute(s).fetchone()
    result_list  = [r for r in result][2:]
    v1 =  np.array(result_list)
    
    s = select([vmat]).where(vmat.c.vid == vid2)
    result = connection.execute(s).fetchone()
    result_list  = [r for r in result][2:]
    v2 =  np.array(result_list)

    if pc*np.dot(u, (v1-v2)) < 1:
        u = u - a*(-pc*(v1-v2) + l*u)
        v1 = v1 - a*(-pc*u + l*v1)
        v2 = v2 - a*(-pc*u + l*v2)
        u = u/np.sum(u)
        v1 = v1/np.sum(v1)
        v2 = v2/np.sum(v2)
        
        insstr = ""
        for i in xrange(fields.K):
            insstr += ("val" + str(i) + "=" + str(u[i]) + ",")
        insstr_eval = "ins = umat.update().where(umat.c.uid == uid).values(" + insstr[:-2] + ")"
        exec(insstr_eval)
        connection.execute(ins)
        
        insstr = ""
        for i in xrange(fields.K):
            insstr += ("val" + str(i) + "=" + str(v1[i]) + ",")
        insstr_eval = "ins = vmat.update().where(vmat.c.vid == vid1).values(" + insstr[:-2] + ")"
        exec(insstr_eval)
        connection.execute(ins)

        insstr = ""
        for i in xrange(fields.K):
            insstr += ("val" + str(i) + "=" + str(v2[i]) + ",")
        insstr_eval = "ins = vmat.update().where(vmat.c.vid == vid2).values(" + insstr[:-2] + ")"
        exec(insstr_eval)
        connection.execute(ins)
        
    return 0

if __name__=='__main__':
    #add_user(1)
    update_choice(2651476,2609108,1)    
