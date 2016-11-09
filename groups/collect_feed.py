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

def collect_data( graph, id, endpoint ):
    return _unfold( graph.get_all_connections( id = id , connection_name=endpoint ) )


if __name__ == '__main__':

    import sys
    import datetime

    for f in sys.argv[1:]:

        for url in open(f):

            try:

                url = url.strip()
                fbid = url.split('?')[0]
                fbid = fbid.split('.com/')[1]
                ## remove list of bad terms
                for s in ['groups/']:
                    fbid = fbid.replace(s, '')
                fbid = fbid.replace('/', '')


                fbobject = graph.get_object(id= fbid, fields='id,name', metadata = '1')
                fbid = fbobject['id']
                fbtype = fbobject['metadata']['type']

                data = {}

                data['name'] = fbobject['name']
                data['id'] = fbid
                data['meta'] = {}
                data['meta']['type'] = fbtype
                data['meta']['url'] = url
                data['meta']['input_file'] = f
                data['meta']['timestamp'] = str( datetime.datetime.now() ) ## when data was collected

                ## todo: store url as well

                ## redo for clarity later
                if fbtype in ['page', 'group', 'event', 'user']:
                    data['feed'] = collect_feed( graph, fbid )

                if fbtype in ['page', 'event']:
                    data['photos'] = collect_data( graph, fbid, 'photos' )

                if fbtype == 'group':
                    data['__members'] = collect_data( graph, fbid, 'members')

                ## TODO: add group and page metadata collection

                json.dump( data, open( 'data/data_' + fbobject['name'].replace(' ', '_').replace('/', '_').lower() + '.json', 'w' ) )


            except facebook.GraphAPIError as e:
                print url, 'failed'
                print e
