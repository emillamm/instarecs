instarecs
=========

A shortcut to powerful recommendations using pairwise comparisons instead of ratings. A live implementation of the algorithm can be found on flicked.co. 

# Intro #
Instarecs is a python implementation of a collaborative filtering algorithm that is based on pairwise comparisons instead of ratings (Usually collaborative filters relies on ratings or likes/dislikes). The purpose of using comparisons instead of ratings, is to eliminate the bias that typically is associated with ratings. 

Instarecs is purely written in Python and all data is stored in MongoDB. 

# Prerequisites #
Following Python libraries are needed: 
- annoy (also depends on Boost)
- pymongo
- numpy
- jsonrpclib

An installation of MongoDB is also required. 

# Setup #
To try out instarecs, make sure that MongoDB is running and then simply do the following:
- from the instarecs directory, run the command `mongoimport -d movie_db -c movies --jsonArray movies.json`
- run `python demo_server.py`. 
This will initialize instarecs with a small movie data set from IMDB and start the server for you. 
Then run `python demo_client.py` in a separate new terminal to try out a few comparisons. 

Alternatively you can: 
- Set the `item_db_name` and `item_collection_name` to the name of a db and collection of your choice. Then run `python init_db.py`.

item\_collection\_name must point to a MongoDB collection inside your item\_db\_name database. Every item in the collection must have a field called id (the `_id` field is not enough) with an integer value.  

# Usage #
```python
# Setup a JSON-RPC Client
import jsonrpclib
server = jsonrpclib.Server('http://localhost:8080')

# Add a user
uid = 1
server.add_user(uid)

# Print the rank of top 10 items for that user
result = server.get_rank(1)
print result

# Make a selection for the user (vid1 is preferred over vid2)
update_choice(vid1, vid2, uid)

# Now print the rank again
result = server.get_rank(1)
print result
```

# Theory #
coming soon
