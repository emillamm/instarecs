instarecs
=========

A shortcut to powerful recommendations using pairwise comparisons instead of ratings. A live implementation of the algorithm can be found on [flicked.co](http://flicked.co/). 
![Prediction accuracy](https://raw.github.com/emillamm/instarecs/master/testresults.png)
Chart explained in the "Test Results"

# Intro #
Instarecs is a python implementation of a collaborative filtering algorithm that is based on pairwise comparisons instead of ratings (Usually collaborative filters relies on ratings or likes/dislikes). The purpose of using comparisons instead of ratings, is to eliminate the bias that typically is associated with ratings. 

Instarecs is purely written in Python and all data is stored in MongoDB. 

# Prerequisites #
Following Python libraries are needed: 
- [annoy](https://github.com/spotify/annoy) (also depends on Boost)
- [pymongo](https://github.com/mongodb/mongo-python-driver)
- [numpy](http://www.numpy.org/)
- [jsonrpclib](https://github.com/joshmarshall/jsonrpclib)

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

# Test Results #
The image on top of the page, demonstrates how instarecs performs on a real world dataset. The graph should be interpreted as such:
Given N items and M users, present the each user with a pair of items and let the user choose which one she likes the most. Compare her choice with the a "guess" made by the algorithm. The guess is simply made by choosing the one of two items that has the best rank. 

So the chart shows that after a user has evaluated around 14 pairs, the algorithm can predict the users next choice with an accuracy of approximately 60%. 

The dataset used is the public available [Jester](http://goldberg.berkeley.edu/jester-data/) dataset that consists of 100 jokes rated by 24,983 users on a rating scale from -10 to +10 (only a subset of 700 users were used). A comparison between two items was simulated by considering the difference in rating scores between the items. This is not the optimal kind of dataset, but it is sufficient to demonstrates capabilities of the algorithm. 

# Theory #
![Prediction accuracy](https://raw.github.com/emillamm/instarecs/master/theory.jpg)