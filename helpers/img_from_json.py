#!/usr/bin/env python

"""Get image posters from omdbapi

This module retrieves images for all movies
in the file "movies.json" and stores them in folder
called images. 

Todo: Use imdb_ids.txt instead of movies.json

NOTE: This file does not handle all errors.  
"""
import urllib2
import json
import pprint
import os

def download_image(movie_name, movie_year, movie_id):
    content_url = "http://www.omdbapi.com/?t=" + movie_name + "&y=" + movie_year

    data = ""
    try:
        content = urllib2.urlopen(content_url).read()
        data = json.loads(content)
    except:
        write_error("("+ str(movie_id) + ", " + movie_name + ") unable to find ID from title and year")
        pass
    
    url = ""
    if(data!=""):
        try:
            url = data["Poster"]
        except:
            write_error("("+ str(movie_id) + ", " + movie_name + ") unable to read image url")
            pass

    if(url!=""):
        # Get images with a height of 300 pixels. 
        url = url.replace("SX300.jpg", "SY300.jpg")
        print(url)
        file_name = "images/" + movie_id + ".jpg"
        try:
            u = urllib2.urlopen(url)
            f = open(file_name, 'wb')
            f.write(u.read())
            f.close()
        except: 
            write_error("("+ str(movie_id) + ", " + movie_name + ") unable write image file")
            pass

def write_error(msg):
    # Write an error message if the image for some reason cant be found
    with open("img_errors.txt", "a") as f:
        f.write(msg.encode('utf8') + "\n")
        f.close
        print(msg.encode('utf8'))

if __name__ == '__main__':
    json_data = open('movies.json','r')
    json_object = json.load(json_data)
    directory = "images"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for row in json_object:
        if not os.access("images/" + str(row['id']) + ".jpg", os.R_OK):
            download_image(row['title'].replace(' ','+'), str(row['year']), str(row['id']))
