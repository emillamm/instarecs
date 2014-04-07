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


fname = "imdb_ids.txt"
f = open(fname)
for line in f:
	ids = line.split(" ")
	_id = ids[0]
	imdbid = re.sub("\D", "", ids[1])
	movie = ia.get_movie(imdbid)
	#plot = get_plot(movie)
	#db.movies.update({"id": int(_id)}, {"$set": {"plot": plot}})
	genres = get_genres(movie)
	db.movies.update({"id": int(_id)}, {"$set": {"genres": genres}})