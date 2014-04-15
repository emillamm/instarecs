#!/usr/bin/env python

"""Get ids from omdbapi

This module is necessary because IMDB doesn't store the real movie
ids in their interface dumbs. See also imdbsql_to_json.py. 
Given a file called "movie.json", retrive imdb ids (those that
are displayed in the url of a movie on www.imdb.com). 
Print all imdb ids in a file called "imdb_ids.txt"
The format of movie.json is as below:

[
    {
        id: 12345,
        title: 'some name',
        year: 1998
    },
    ...
]

If unable to find the imdb id from omdbapi, an error 
message is printed in the file instead. 

NOTE: This file does not handle all errors.  
"""
import urllib2
import json
import pprint
import os


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

if __name__ == '__main__':
    json_data = open('movies.json','r')
    json_object = json.load(json_data)
    for row in json_object:
        get_id(row['title'].replace(' ','+'), str(row['year']), str(row['id']))
