import json
from pprint import pprint

data = json.load(open('player.json'))

pprint (data['Stephen Curry'])

i =0
for key in data.keys():
	if "Kadeem Allen" in key:
		print i, key
	i+=1

import basketballCrawler as bc

#players = bc.buildPlayerDictionary()

players = bc.loadPlayerDictionary("player.json")
print players['LeBron James'].gamelog_url_list

#for key in players.keys():
#	print key.decode('utf-8')
print len(players.keys())