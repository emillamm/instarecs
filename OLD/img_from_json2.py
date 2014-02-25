#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import imdb
import urllib2

access = imdb.IMDb()
movie = access.get_movie(1132626)
movie = access.search_movie('The matrix')

page = urllib2.urlopen(access.get_imdbURL(movie))
soup = BeautifulSoup(page)
cover_div = soup.find(attrs={"class" : "image"})
cover_url = (cover_div.find('img'))['src']
print "Cover url: %s" % cover_url
