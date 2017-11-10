"""

Rest API that provides calls to the database.

"""

import json
import pickledb
from flask import Flask, Response, request


number_of_current_users = 0
current_user_database = pickledb.load ("current_users.txt", False)
current_user_position = 0

app = Flask(__name__)

@app.route("/test")
def test():
        return 'hello there'


@app.route('/CurrentUsers/Add', methods = ['POST'])
def addCurrentUser():
	global current_user_position
	username = request.json['username']
	score = request.json['score']
	if not current_user_database.get('current_user_list'):
		current_user_database.lcreate ('current_user_list')
	if not current_user_database.get('current_user_pos_list'):
		current_user_database.lcreate ('current_user_pos_list')
	current_user_database.ladd ('current_user_list', username)
	current_user_database.ladd('current_user_pos_list', username + '_pos')
	current_user_database.set (username+'_pos' , current_user_position)
	current_user_database.set (request.json['username'] , request.json['score'])
	current_user_database.dump()
	current_user_position+=1
	
	return	str(request.json)

@app.route('/CurrentUsers/GetPosition', methods = ['POST'])
def getPosition():
	username = request.json['username']
	username+='_pos'
	return str (current_user_database.get(username))


@app.route('/CurrentUsers/Delete', methods = ['POST'])
def deleteCurrentUser ():
	username = request.json['username']
	


	current_user_database.rem(username)

	username+='_pos'
	pos = current_user_database.get(username)

	current_user_database.rem(username)


	current_user_database.lpop('current_user_list', pos)
	current_user_database.lpop('current_user_pos_list',pos)


	
	

	# Update the rest of the positions
	for i in range (0, current_user_database.llen('current_user_pos_list')):
		username_pos = current_user_database.lget('current_user_pos_list',i)
		value = (current_user_database.get(username_pos))
		if  (value > pos):

			value  = value - 1
			current_user_database.set(username_pos, value  )


	current_user_database.dump()
	return str('trye')
	

@app.route("/getCurrentUsers")
def getCurrentUsers():
	db = pickledb.load("current_users.txt", False)
	keys = db.getall()
        data = {}
        for key in keys:
                data[key] = db.get(key)
        resp_content = json.dumps(data)         
        
        return Response(response=resp_content, status=200, mimetype="application/json")


@app.route('/HighScoreData/Add', methods = ['POST'])
def addScoreData ():
	db = pickledb.load ("database.txt", False)
	db.set (request.json['username'], request.json['score'])
	db.dump()
	return str(request.json)


@app.route('/HighScoreData/Get', methods = ['GET'])
def getAllHighScoreData ():	
	db = pickledb.load("database.txt", False)
	keys = db.getall()
	data = {}
	for key in keys:
		data[key] = db.get(key)
	resp_content = json.dumps(data)		
	return Response(response=resp_content, status=200, mimetype="application/json")


if	__name__ == '__main__':

	print "Create List"
