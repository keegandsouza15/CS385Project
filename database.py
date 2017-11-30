"""
Rest API that provides calls to the database.
"""

import json 
from flask import Flask, Response, request
from cassandra.cluster import Cluster


cluster = Cluster()
session = cluster.connect('highscoredata')


app = Flask(__name__)

@app.route("/test")
def test():
	return 'hello there'

@app.route('/CurrentUsers/Get', methods = ['GET'])
def getCurrentUsers ():
	r = ''
	rows = session.execute('select * from currentUsers;')
	for row in rows:
		r += str(row)
	return r
@app.route('/CurrentUsers/Add', methods = ['POST'])
def addCurrentUser ():
	username = request.json['username']
	score = request.json['score']
	session.execute('INSERT INTO currentUsers (currentusers_username, currentusers_score) VALUES (%s, %s)', (username, score))
	return str(request.json)

@app.route('/CurrentUsers/Delete', methods = ['POST'])
def deleteCurrentUser ():
	username = request.json['username']
	session.execute('DELETE FROM currentUsers WHERE currentusers_username=%s', (username,))
	return str(request.json)

@app.route('/CurrentUsers/Update', methods = ['POST'])
def updateCurrentUser ():
	username = request.json['username']
	score = request.json['score']
	session.execute('UPDATE currentUsers SET currentusers_score=%s WHERE currentusers_username=%s', (score, username))
	return str(request.json)

@app.route('/CurrentUsers/GetPosition', methods =['POST'])
def getCurrentPosition ():
	count = 0
	score = request.json['score']
	rows = session.execute('SELECT * FROM currentUsers WHERE currentusers_score >= %s ALLOW FILTERING', (score,))
	for row in rows:
		count += 1
	return str(count)

@app.route('/HighScores/Get', methods = ['GET'])
def getHighScoreUsers ():
	r = ''
	rows = session.execute('select * from highScores;')
	for row in rows:
		r += str(row)
	return r
@app.route('/HighScores/Add', methods = ['POST'])
def addHighScoreUser ():
	username = request.json['username']
	score = request.json['score']
	session.execute('INSERT INTO highScores (highScores_username, highScores_score) VALUES (%s, %s)', (username, score))
	return str(request.json)

@app.route('/HighScores/Find', methods = ['POST'])
def findHighScoreUser ():
	username = request.json['username']
	rows = session.execute('SELECT * FROM highScores WHERE highscores_username=%s', (str(username)))
	if not rows:
	    	return 'False'
	return 'True'

@app.route('/HighScores/GetPosition', methods =['POST'])
def getHighScorePosition ():
	count = 0
	score = request.json['score']
	rows = session.execute('SELECT * FROM highScores WHERE highScores_score >= %s ALLOW FILTERING', (score,))
	for row in rows:
		count += 1
	return str(count)
