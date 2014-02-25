#!/usr/bin/env python

import urllib2
import json
import pprint
import os


"""Get image poster from rotten tomatoes"""




def download_image(movie_name, movie_year, movie_id):
    apikey = "3pz99vvewyny65r2uccm66zy"
    content_url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=" + apikey + "&q=" + movie_name + "+" + movie_year + "&page_limit=1"
    #print(content_url)
    data = ""
    try:
        content = urllib2.urlopen(content_url).read()
        data = json.loads(content)
    except:
        write_error("("+ str(movie_id) + ", " + movie_name + ") unable to open url or load json: " + content_url)
        pass
    
    url = ""
    try:
        url = data["movies"][0]["posters"]["original"]
    except:
        write_error("("+ str(movie_id) + ", " + movie_name + ") unable to read image url")
        pass

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
    with open("img_errors.txt", "a") as f:
        f.write(msg.encode('utf8') + "\n")
        f.close
        print(msg.encode('utf8'))

json_data = open('movies.json','r')
json_object = json.load(json_data)
count = 0
for row in json_object:
    #if count >= 0 and count < 302 and not os.access("images/" + str(row['id']) + ".jpg", os.R_OK):
    if not os.access("images/" + str(row['id']) + ".jpg", os.R_OK):

        download_image(row['title'].replace(' ','+'), str(row['year']), str(row['id']))
    count = count + 1

