"""Retrieving all choice updates from all users

This module simply takes all updates that has been made so far
and puts them in a text called "survey.txt file where each line has the format:

<uid> <vid1> <vid2>

Remember that vid1 is then one that is preferred ocer vid2. 
An update is simply a call to the update_choice function in api.py. 

NOTE: This file does not handle all errors.  
"""


from pymongo import MongoClient
import os

conn = MongoClient()
db = conn.instarecs
fname = "survey.txt"

def parse_survey_results():
	if os.path.isfile(fname):
		os.remove(fname)	
	survey_results = db.survey.find()
	for survey in survey_results:
		for c in survey["choice"]:
			write_result(str(survey["uid"]) + " " + str(c["vid1"]) + " " + str(c["vid2"]))

def write_result(result):
	with open(fname, "a") as f:
		f.write(result.encode('utf8') + "\n")
		f.close
		print(result.encode('utf8'))

if __name__=='__main__':
	parse_survey_results()
