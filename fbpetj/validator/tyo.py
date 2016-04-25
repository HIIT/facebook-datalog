# -*- coding: utf-8 -*-

# use function tyo (file name as argument) to validate json created by fbpetj

def tyo(file):

	import json

	f = open(file, 'r')

	f_read = f.read()

	f.close()

	f_read = json.loads(f_read)

	#Tarkistaa onko rsvp_status in participation
	for x in f_read['participation']:
		if not 'rsvp_status' in x:
			print 'Puuttuu rsvp',x

	#Onko ID in participation
	for x in f_read['participation']:
		if not 'id' in x:
			print 'Puuttuu Participation id',x

	#Onko nimeä in participation
	for x in f_read['participation']:
		if not 'name' in x:
			print 'Puuttuu Participation Nimi',x

	#Onko Likes in Feed
	for x in f_read['feed']:
		if not 'likes' in x:
			print 'Puuttuu Feed Like',x

	#Onko Like ID in Feed
	for x in f_read['feed']:
		for o in x['likes']:
			if not 'id' in o:
				print 'Puuttuu Feed Like ID',o

	#Onko Message, Story tai Link in Feed
	#for y in f_read['feed']:
		#if not 'message' in y and not 'story' in y and not 'link' in y:
			#print 'Puuttuu Feed Message, Story tai Link',y

	#Onko Commenttia in Feed
	for y in f_read['feed']:
		if not 'comments' in y:
			print 'Puuttuu Feed Comment',y

	#Onko Commentti Likea (in Feed)
	for y in f_read['feed']:
		for x in y['comments']:
			if not 'likes' in y:
				print 'Puuttuu Comment Like in Feed',y

	#Onko Comment Like ID (in Feed)
	for y in f_read['feed']:
		for x in y['comments']:
			for o in x['likes']:
				if not 'id' in o:
					print 'Puuttuu Comment Like ID in Feed',o

	#Onko Commentissa Message, Time ja ID (in Feed)
	for y in f_read['feed']:
		for x in y['comments']:
			if not 'message' in x or not 'created_time' in x or not 'id' in x:
				print 'Puuttuu Comment Message, Time tai ID',x

	#Onko Commentissa From (in Feed)
	for y in f_read['feed']:
		for x in y['comments']:
			if not 'from' in x:
				print 'Puuttuu Comment lähettäjä (in feed)',x

	#Onko Commentissa from ID
	for y in f_read['feed']:
		for x in y['comments']:
			if not 'id' in x['from']:
				print 'Puuttuu Comment lähettäjä ID',o

	#Onko ID in Feed
	for y in f_read['feed']:
		if not 'id' in y:
			print 'Puuttuu Feed ID',y

	#Onko time in feed
	for y in f_read['feed']:
                if not 'created_time' in y:
                        print 'Puuttuu Time in Feed',y
