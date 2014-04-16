#!/usr/bin/env python
"""Simple script for testing the server"""
from lib import fields
from pymongo import MongoClient

# DB connection
conn = MongoClient()
db_movies = conn[fields.item_db_name]

# Setup a JSON-RPC Client
import jsonrpclib
server = jsonrpclib.Server('http://localhost:8080')

# Add a user
uid = 1
server.add_user(uid)

# Print the rank of top 10 items for that user
print 'This is the initial ranking of movies:'
result = server.get_rank(1)
for row in result:
	print db_movies[fields.item_collection_name].find({'id': row})[0]['title']

# Make a selection for the user (vid1 is preferred over vid2)
vid1 = result[0]
vid2 = result[1]
server.update_choice(vid1, vid2, uid)

# Now print the rank again
print '\nThis is the new ranking after the last movie was preffered over the first:'
result = server.get_rank(1)
for row in result:
	print db_movies[fields.item_collection_name].find({'id': row})[0]['title']

