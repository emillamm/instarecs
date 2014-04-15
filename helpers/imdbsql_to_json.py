#!/usr/bin/env python

"""Retrieve movies from MySQL DB that is storing a version
of the IMDB interface (http://www.imdb.com/interfaces). 

This module simply converts SQL movies to JSON format and 
stores the movies in a file called "movies.json". 
Remember to replace the connection string with variables 
corresponding to your DB. 

NOTE: This file does not handle all errors. 
"""

import sys
from sqlalchemy import *
import json
import collections

def make_json():
    engine = create_engine('mysql://user:pass@ip/db')
    connection = engine.connect()
    # This is just a custom SQL query that can be replaced depending on
    # which movies you want in your file. 
    q = """select t.title, t.production_year as year, m1.info as count, m2.info as rating, m1.movie_id as id
    from title t 
    inner join movie_info_idx m1 on t.id=m1.movie_id and m1.info_type_id = 100
    inner join movie_info_idx m2 on t.id=m2.movie_id and m2.info_type_id = 101
    where t.kind_id = 1 and m1.info > 200000 and m1.info < 250000 order by m1.info asc limit 100;"""
    result = engine.execute(q)

    item_list = []
    for row in result:
        o = collections.OrderedDict()
        o['id'] = row["id"]
        q = "select title from aka_title where movie_id = " + str(row["id"]) + " and note like \"(USA)\";"
        result_tmp = engine.execute(q)

        # Get english title, if it exists (sometimes)
        # IMDB displays their title in a foreign language.
        title_eng = result_tmp.fetchone()
        if not title_eng  == None:
            o['title'] = title_eng[0].decode("ISO-8859-1")
        else:   
            o['title'] = str(row["title"]).decode("ISO-8859-1")
        # Currently only these fields are stored besides
        # the title and ID. 
        o['year'] = row["year"]
        o['count'] = row["count"]
        o['rating'] = row["rating"]
        
        item_list.append(o) 
        
    j = json.dumps(item_list)
    objects_file = 'movies.json'
    f = open(objects_file,'w')
    print >> f, j
         
if __name__ == '__main__':
    make_json()
