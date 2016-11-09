import sys
sys.path.insert( 0, '/Users/mnelimar/code/facebook-sdk/' ) ## temporary hack to use newer version of SDK

import facebook
import requests
import json

keys = json.load( open('keys.json') )
app_id = keys['app-id']
app_secret = keys['app-secret']

__DEV__ = True ## Flag to test if we're running a development thing => limit the amount of data collected from feeds

graph = facebook.GraphAPI(access_token= app_id + '|' + app_secret, version='2.7')

def _unfold( generator ): ## TODO: this shoud not be needed really
    r = []
    for i in generator:
        r.append( i )
    return r

def collect_feed( graph, id ):

    ## collect posts
    data = {}

    if __DEV__:

        posts = graph.get_connections( id = id , connection_name='feed' ) ## approximately 25
        posts = posts['data']

    else:
        posts = _unfold( graph.get_all_connections( id = id , connection_name='feed' ) )

    for post in posts:

        data[ post['id'] ] =  graph.get_object( post['id'] ,
            fields ='id,from,created_time,application,description,message,to,updated_time'
        ) ## to be compleated

        data[ post['id'] ][ '__comments' ] = _unfold( graph.get_all_connections( id = post['id'], connection_name='comments' ) )
        data[ post['id'] ][ '_likes' ] = _unfold( graph.get_all_connections( id = post['id'], connection_name='likes' ) )

    return data.values()

def collect_group( graph, id, data ):
    ## items particular to a group
    data['__members'] = _unfold( graph.get_all_connections( id = id , connection_name='members' ) )


for line in open('wave0.txt'):

    try:

        line = line.strip()
        line = line.split('?')[0]
        line = line.split('.com/')[1]
        ## remove list of bad terms
        for s in ['groups/']:
            line = line.replace(s, '')
        line = line.replace('/', '')

        print line

        fbobject = graph.get_object(id= line, fields='id,name', metadata = '1')
        fbid = fbobject['id']
        fbtype = fbobject['metadata']['type']

        data = {}

        data['name'] = fbobject['name']
        data['id'] = fbid
        data['type'] = fbtype
        ## todo: store url as well

        if fbtype in ['page', 'group', 'event', 'user']:
            data['feed'] = collect_feed( graph, fbid )

        if fbtype == 'group':
            collect_group( graph, fbid, data )

        ## TODO: add group and page metadata collection

        json.dump( data, open( 'data/data_' + fbobject['name'].replace(' ', '_').replace('/', '_').lower() + '.json', 'w' ) )


    except facebook.GraphAPIError:
        print line, 'failed'
