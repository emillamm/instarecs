#!/usr/bin/env python
import urllib2
import json
import pprint
import os

"""Get ids from omdbapi"""


def get_id(movie_name, movie_year, movie_id):
    content_url = "http://www.omdbapi.com/?t=" + movie_name + "&y=" + movie_year

    data = ""
    try:
        content = urllib2.urlopen(content_url).read()
        data = json.loads(content)
    except:
        write_id_line(str(movie_id) + " " + movie_name + " - unable to find ID from title and year")
        pass
    
    imdbid = ""
    if(data!=""):
        try:
            imdbid = data["imdbID"]
        except:
            write_id_line(str(movie_id) + " " + movie_name + " - unable to read imdbID")
            pass

    if(imdbid!=""):
        write_id_line(str(movie_id) + " " + str(imdbid))

def write_id_line(msg):
    with open("imdb_ids.txt", "a") as f:
        f.write(msg.encode('utf8') + "\n")
        f.close
        print(msg.encode('utf8'))

json_data = open('movies.json','r')
json_object = json.load(json_data)
for row in json_object:
    get_id(row['title'].replace(' ','+'), str(row['year']), str(row['id']))
