#/usr/bin/env python

"""API module

All algorithm level API functions are specified in this module. 
update_choice and get_rank are the primus motor functions in 
Instarecs. 
"""
import json
from fields import *
import random
from annoy import AnnoyIndex
from pymongo import MongoClient
import numpy as np

# Setup DB connection
conn = MongoClient()
db = conn.instarecs

def add_user(uid):
    """Add a user to the DB given an existing unique user ids

    A user is added to the database by generating a random feature vector. 
    The dimensionality of the features set in the file fields.py. 

    Args: 
        uid (int): User ID

    Returns: 
        True if successful, False otherwise
    """ 
    # Generate a set of features
    rand_features = [random.random() for i in xrange(data_dimension)]
    # Normalize the feature vector. 
    rand_features = rand_features/np.sum(rand_features)
    try:
        db.users.update({"uid": uid}, {"uid": uid, "vals": rand_features.tolist()}, upsert=True)    
    except TypeError:
        print "Unable to insert user given uid"
        return False
    return True

def update_choice(vid1, vid2, uid):
    """Update user and item feature vectors given a users choice between two items

    When the user chooses one of two items, the user/item feature vectors are
    updated by using Stochastic Gradient Descent and a hinge loss function. 

    Args: 
        vid1 (str): ID of the PREFERRED item
        vid2 (str): ID of the NON-PREFERRED item
        uid (int): User ID

    Returns: 
        True if successful, False otherwise

    """
    # pc = 1 means that the user chose vid1 over vid 2. (pc can be 1 or -1). 
    pc = 1.0
    # Select user and item feature vectors from the DB
    try: 
        u =  np.array(db.users.find({"uid": uid})[0]["vals"])
        v1 =  np.array(db.items.find({"vid": vid1})[0]["vals"])
        v2 =  np.array(db.items.find({"vid": vid2})[0]["vals"])
    except TypeError:
        print "Unable to fetch user/items from DB"
        return False
    # Update step of the algorithm
    if pc*np.dot(u, (v1-v2)) < 1.0:
        u = u - alpha_u*(-pc*(v1-v2) + lambd*u)
        v1 = v1 - alpha_v*(-pc*u + lambd*v1)
        v2 = v2 - alpha_v*(-pc*u + lambd*v2)
        u = u/np.sum(u)
        v1 = v1/np.sum(v1)
        v2 = v2/np.sum(v2)
        try: 
            db.users.update({"uid": uid}, {"$set": {"vals": u.tolist()}})
            db.items.update({"vid": vid1}, {"$set": {"vals": v1.tolist()}})
            db.items.update({"vid": vid2}, {"$set": {"vals": v2.tolist()}})
            db.survey.update({"uid": uid}, { "$push" : { "choice" : { "vid1" : vid1, "vid2" : vid2}}}, upsert=True)
        except TypeError:
            print "Unable to update feature vectors in DB"
            return False
    return True

def get_rank(uid):
    """Returns a list of the 10 best ranked items for a user

    This function generates a rank of items for a given user by using 
    Approximate Nearest Neighbours. The algorithm
    is imported from the Annoy library (developed by Spotify). 
    
    Todo: The index is built from scratch everytime the function is called, 
    which definitely should be changed in the future for increased performance. 
    It should be fairly easy to do as ANNOY can store indexes in files which can
    easily been shared by processes. However, it works well with a few hundred items
    as it is now. 

    item_queue: It is a list of item ids for each user. It acts as a circular queue
    for keeping track of which items the user has seen so far. When two new items are 
    shown to the user, they are placed in the back of the queue. 

    Args:
        uid (int): User ID

    Returns: 
        List of item ids (str)
    """
    ann = AnnoyIndex(data_dimension)
    try:
        items = db.items.find()
        q = db.users.find({"uid": uid}, {"item_queue" : 1, "_id": 0})[0]["item_queue"]
    except TypeError:
        print "Unable to fetch user from DB"
    ids = [i["vid"] for i in q ]
    # Following line can be deleted or modified. 
    # It removes the last 15 items from the ANN tree, so they will never be recommended
    # for the user. This is done to make sure the user only sees new items in the 
    # recommended list (assuming 15 is the number of comparisons the user has made). 
    ids[-15:] = []
    print ids
    id_dict = {}
    # Add items to ANN tree
    for i,item in enumerate(items):
        if item["vid"] in ids:
            # Store all ids in a dictionary
            id_dict[str(i)] = item["vid"]
            ann.add_item(i, item["vals"])
    # Erik Bernhardson (aurthor of ANNOY) suggests to use 2*dimension of data as the number
    # of trees to build. 
    ann.build(data_dimension*2)
    try: 
        user = db.users.find({"uid": uid})[0]
    except TypeError:
        print "Unable to fetch user from DB"
    # Get 10 highest ranked items for that user
    nns_tmp = ann.get_nns_by_vector(user["vals"],10)
    nns = [id_dict[str(k)] for k in nns_tmp]
    print nns
    return nns

def get_random_pair(uid):
    """Returns a pair of items to be compared by the user. 

    The items is randomly chosen with the constraint of never showing 
    2 of the same items for the user (As described in 'item_queue' in the 
    get_rank function).

    Todo: The pop/append call can be optimized by doing it directly 
    on the document in mongoDB (never retrieving it from the DB first). 
    
    Args:
        uid (int): User ID

    Returns: 
        pair of item ids (str) in a list
    """
    ids = []
    try: 
        q = db.users.find({"uid": uid}, {"item_queue" : 1, "_id": 0})[0]
    except TypeError:
        print "Unable to fetch user from DB"
    # If new user, add a field called item_queue with list of ids. 
    # Else retrieve current item_queue on user. 
    if q.get('item_queue') == None:
        try:
            ids = list(db.items.find({}, {"vid": 1, "_id": 0}))
        except TypeError:
            print "Unable to fetch item from DB"
        random.shuffle(ids)
    else:
        ids = q["item_queue"]
    # Pick two fron most items and push them back in the queue. 
    vid1 = ids.pop(0)
    vid2 = ids.pop(0)
    ids.append(vid1)
    ids.append(vid2)
    db.users.update({"uid": uid}, {"$set": {"item_queue": ids}})
    pair = [vid1, vid2]
    return pair

if __name__=='__main__':
    pass