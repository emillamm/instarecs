#!/usr/bin/env python
from fields import *
import random
from pymongo import MongoClient
import numpy as np

"""Initialize database with random feature vectors

Features are sampled from a uniform distribution and 
vectors are normalized afterwards. 
"""
# Setup DB connection
conn = MongoClient()
db = conn.instarecs

def populate_data():
    db_movies = conn[item_db_name]
    db.items.remove()
    items = db_movies[item_collection_name].find()
    for item in items:
        rand_features = [random.random() for i in xrange(data_dimension)]
        rand_features = rand_features/np.sum(rand_features)
        db.items.insert({"vid": item["id"], "vals": rand_features.tolist()})


if __name__ == '__main__':
    populate_data()