import sys
sys.path.insert( 0, '/Users/mnelimar/code/facebook-sdk/' ) ## temporary hack to use newer version of SDK

import facebook
import requests
import json
import time

keys = json.load( open('keys.json') )
app_id = keys['app-id']
app_secret = keys['app-secret']

__DEV__ = False ## True ## Flag to test if we're running a development thing => limit the amount of data collected from feeds

graph = facebook.GraphAPI(access_token= app_id + '|' + app_secret, version='2.7')

def collect_feed( fbid ):

    ## collect posts
    data = {}

    if __DEV__:

        posts = graph.get_connections( id = fbid , connection_name='feed' ) ## approximately 25
        posts = posts['data']

    else:
        posts = collect_data( fbid , 'feed' )

    for post in posts:

        try:

            data[ post['id'] ] =  graph.get_object( post['id'] ,
                fields ='id,from,created_time,application,description,message,to,updated_time'
            ) ## to be compleated

            data[ post['id'] ][ 'comments' ] = collect_data( post['id'], 'comments' )
            data[ post['id'] ][ 'likes' ] = collect_data( post['id'], 'likes' )

        except facebook.GraphAPIError as e:
            print e
            data[ post['id'] ] = { 'id' : post['id']  }

    return data.values()

def collect_data( fbid, endpoint ):
    ret = []

    try:
        d = graph.get_all_connections( id = fbid , connection_name=endpoint )
        for _d in d:
            ret.append( _d )
    except facebook.GraphAPIError as e:
        if e.code in [4, 17, 341]: ## application limit errors
            time.sleep( 60 * 60 ) ## one hour
            return collect_data( fbid, endpoint )
        else:
            print "Error", e

    finally:
        return ret


def collect_basics( fbid ):

    try:

        fbobject = graph.get_object(id= fbid, fields='id,name', metadata = '1')
        fbid = fbobject['id']
        fbtype = fbobject['metadata']['type']

        data = {}

        data['name'] = fbobject['name']
        data['id'] = fbid
        data['meta'] = {}
        data['meta']['type'] = fbtype
        ## data['meta']['url'] = url         ## todo: store url as well
        data['meta']['input_file'] = f
        data['meta']['collection_time'] = str( datetime.datetime.now() ) ## when data was collected

        return data

    except facebook.GraphAPIError as e:
        if e.code in [4, 17, 341]: ## application limit errors
            time.sleep( 60 * 60 ) ## one hour
            return collect_basics( fbid )
        else:
            print "Error", e


if __name__ == '__main__':

    import sys
    import datetime

    for i, filename in enumerate( sys.argv[1:] ):

        for j, url in enumerate( open(filename) ):

            print "File", i, "entry", j

            url = url.strip()
            fbid = url.split('?')[0]
            fbid = fbid.split('.com/')[1]
            ## remove list of bad terms
            for s in ['groups/']:
                fbid = fbid.replace(s, '')
            fbid = fbid.replace('/', '')

            data = collect_basics( fbid )

            fbtype = data['meta']['type']
            if fbtype in ['page', 'group', 'event', 'user']:
                data['feed'] = collect_feed( fbid )

            if fbtype in ['page', 'event']:
                data['photos'] = collect_data( fbid, 'photos' )

            if fbtype == 'group':
                data['members'] = collect_data( fbid, 'members')

            ## TODO: add group and page metadata collection

            json.dump( data, open( 'data/data_' + fbobject['name'].replace(' ', '_').replace('/', '_').lower() + '.json', 'w' ), sort_keys=True, indent=4 )
