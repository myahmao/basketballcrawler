import json
from pprint import pprint
from nba_py import player
import pymongo
from pymongo import MongoClient

data = json.load(open('player.json'))

#pprint (data['Stephen Curry'])

i =0
for key in data.keys():
	if "Kadeem Allen" in key:
		print i, key
	i+=1

import basketballCrawler as bc

#players = bc.buildPlayerDictionary()
'''
        self.positions = []
        self.height = None
        self.weight = None
        self.overview_url_content = None
        self.gamelog_data = None
        self.gamelog_url_list = []
'''

client = MongoClient('34.212.20.96', 27017)
coll_name = 'Player'
db = client['nba_player']
#db.authenticate(user[1], user[2])
collection = db[coll_name]

players = bc.loadPlayerDictionary("player.json")
#print players['LeBron James'].overview_url

for key in players.keys():
	positions = players[key].positions

	player_name =  str(key.decode('utf-8')).title()
	height = players[key].height
	weight = players[key].weight

	name = str(key.decode('utf-8')).split(' ')
	firstname = name[0]
	if len(name) == 2:
		lastname = name [1] 
	if len(name) == 3:
		if 'Jr' in name[2]:
			lastname = name[1].strip(',')
			print lastname
		else :
			lastname = name[2]
			midname = name[1]

	firstname = firstname.title()
	lastname = lastname.title()
	print firstname,lastname

	#userRecord = collection.find_one({'lastname': lastname, 'firstname': firstname})
	#if not userRecord:
	
	collection.insert({'firstname'    : firstname,
                           'lastname'   : lastname,
                           'name': player_name,
                           'height'   : height,
                           'weight'   : weight,
                           'positions' : positions,
                          })
    
	#print len(players.keys())
	'''
	try:
		get_player = player.get_player(firstname, last_name=lastname)
		#print get_player

		player_id = get_player.values[0]
		#print player_id
		player_summary = player.PlayerSummary(player_id)
		team_name = player_summary.info()["TEAM_CITY"][0] +' '+ player_summary.info()["TEAM_NAME"][0]

		print firstname, lastname+':', team_name

		userRecord = collection.find_one({'lastname': lastname, 'firstname': firstname})
		if userRecord:
	
			collection.update_one(
                  {'lastname': lastname, 'firstname': firstname},
                  {
                    "$set" :  {'team':team_name,
                              },
                  }
                )
	except:
		print 'player not found'
	'''