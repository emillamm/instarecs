"""Retrieve movie information from imdbpy and store it in MongoDB

This is simply a module that connects to IMDB via the
imdbpy library and stores all info in a MongoDB database
Currently only plot and genres are fetched. 

NOTE: This file does not handle all errors.  
"""
import imdb
import re
from pymongo import MongoClient

ia = imdb.IMDb()
conn = MongoClient()
db = conn.flickfind

def get_plot(movie):
	plot = movie.get('plot outline')
	print plot
	return plot

def get_genres(movie):
	genres = movie.get('genre')
	print genres
	return genres

if __name__ == '__main__':
	fname = "imdb_ids.txt"
	f = open(fname)
	for line in f:
		ids = line.split(" ")
		_id = ids[0]
		# Remove all letters from the ID. Whe only need the digits. 
		imdbid = re.sub("\D", "", ids[1])
		movie = ia.get_movie(imdbid)
		plot = get_plot(movie)
		db.movies.update({"id": int(_id)}, {"$set": {"plot": plot}})
		genres = get_genres(movie)
		db.movies.update({"id": int(_id)}, {"$set": {"genres": genres}})