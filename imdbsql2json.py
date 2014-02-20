#!/usr/bin/env python

import sys
import MySQLdb as mdb
from sqlalchemy import *
import json
import collections

def make_json():
    engine = create_engine('mysql://emil:mrmemorex@50.17.252.200/imdb')
    connection = engine.connect()
    q = """select title, production_year as year, m1.info as count, m2.info as rating, m1.movie_id as id
    from title t 
    inner join movie_info_idx m1 on t.id=m1.movie_id and m1.info_type_id = 100
    inner join movie_info_idx m2 on t.id=m2.movie_id and m2.info_type_id = 101
    where t.kind_id = 1 and m1.info > 300000 and m2.info > 8 order by m2.info desc;"""

    result = engine.execute(q)
    item_list = []
    for row in result:
        o = collections.OrderedDict()
        o['id'] = row["id"]
        o['title'] = row["title"].decode("ISO-8859-1")
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
