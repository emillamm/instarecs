#!/usr/bin/env python
"""Algorithm  and DB specific constants. 

These algorithm constants are the default values that seem to work well
for a small dataset of 100 items: 

data_dimension = 8
alpha_u = 1.0
alpha_v = 0.005
lambd = 10.0
"""
### Algorithm
data_dimension = 8
alpha_u = 1.0
alpha_v = 0.005
lambd = 10.0

### DB
# Name of database that contains all the items
# For the demo it is called movies. But name it to what you want. 
item_db_name = 'movie_db'
item_collection_name = 'movies'
