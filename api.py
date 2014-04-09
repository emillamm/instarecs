#/usr/bin/env python
import json
from fields import *
import random
from annoy import AnnoyIndex
from pymongo import MongoClient
import numpy as np

conn = MongoClient()
db = conn.instarecs

def add_user(uid):
    rand_features = [random.random() for i in xrange(data_dimension)]
    rand_features = rand_features/np.sum(rand_features)
    db.users.update({"uid": uid}, {"uid": uid, "vals": rand_features.tolist()}, upsert=True)
    return 0 

def update_choice(vid1, vid2, uid):
    #uid = int(uid)
    print [vid1, vid2, uid]
    pc = 1.0
    # Select user and item feature vectors
    u =  np.array(db.users.find({"uid": uid})[0]["vals"])
    v1 =  np.array(db.items.find({"vid": vid1})[0]["vals"])
    v2 =  np.array(db.items.find({"vid": vid2})[0]["vals"])

    if pc*np.dot(u, (v1-v2)) < 1.0:
        print pc*np.dot(u, (v1-v2))
        u = u - alpha_u*(-pc*(v1-v2) + lambd*u)
        v1 = v1 - alpha_v*(-pc*u + lambd*v1)
        v2 = v2 - alpha_v*(-pc*u + lambd*v2)
        u = u/np.sum(u)
        v1 = v1/np.sum(v1)
        v2 = v2/np.sum(v2)
        
        db.users.update({"uid": uid}, {"$set": {"vals": u.tolist()}})
        db.items.update({"vid": vid1}, {"$set": {"vals": v1.tolist()}})
        db.items.update({"vid": vid2}, {"$set": {"vals": v2.tolist()}})
        db.survey.update({"uid": uid}, { "$push" : { "choice" : { "vid1" : vid1, "vid2" : vid2}}}, upsert=True)
        print u
    return 0

def get_rank(uid):
    # Dimension of our vector space
    ann = AnnoyIndex(data_dimension)
    items = db.items.find()
    q = db.users.find({"uid": uid}, {"item_queue" : 1, "_id": 0})[0]["item_queue"]
    ids = [i["vid"] for i in q ]
    ids[-20:] = []
    print ids
    id_dict = {}
    for i,item in enumerate(items):
        #print item["vid"]
        #print item["vals"]
        if item["vid"] in ids:
            id_dict[str(i)] = item["vid"]
            ann.add_item(i, item["vals"])
    ann.build(data_dimension*2)
    user = db.users.find({"uid": uid})[0]
    nns_tmp = ann.get_nns_by_vector(user["vals"],10)
    nns = [id_dict[str(k)] for k in nns_tmp]
    print nns
    return nns

def get_random_pair(uid):
    #Can be optimized by pushing/popping directly from the queue in MongoDB
    ids = []
    q = db.users.find({"uid": uid}, {"item_queue" : 1, "_id": 0})[0]
    if q.get('item_queue') == None:
        print 'ss'
        ids = list(db.items.find({}, {"vid": 1, "_id": 0}))
        random.shuffle(ids)
    else:
        ids = q["item_queue"]
    vid1 = ids.pop(0)
    vid2 = ids.pop(0)
    ids.append(vid1)
    ids.append(vid2)
    db.users.update({"uid": uid}, {"$set": {"item_queue": ids}})
    pair = [vid1, vid2]
    
    return pair


if __name__=='__main__':
    #add_user(1)
    #update_choice(2651476,2609108,1)    
    get_rank(1396734844)
    #get_random_pair(1396734844)
