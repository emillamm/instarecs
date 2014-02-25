#!/usr/bin/env python

import urllib2
import json
import pprint


"""Get image poster from rotten tomatoes"""




def download_image(movie_name, movie_year, movie_id):
    apikey = "3pz99vvewyny65r2uccm66zy"
    content_url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=" + apikey + "&q=" + movie_name + "+" + movie_year + "&page_limit=1"
    #print(content_url)
    content = urllib2.urlopen(content_url).read()

    data = json.loads(content)
    url = data["movies"][0]["posters"]["original"]
    print(url)
    file_name = "images/" + movie_id + ".jpg"
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            print("none")
            break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,

    f.close()

json_data = open('movies.json','r')
json_object = json.load(json_data)


count = 0
for row in json_object:
    if count < 1:
        download_image(row['title'].replace(' ','+'), str(row['year']), str(row['id']))
    count = count + 1

