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

def handle_fb_errors( e , redo ):
    if e.code in [4, 17, 341]: ## application limit errors
        time.sleep( 60 * 60 ) ## one hour
        redo()
    else:
        print "Error", e


def collect_feed( fbid ):

    ## collect posts
    data = {}

    if __DEV__:

        posts = graph.get_connections( id = fbid , connection_name='feed' ) ## approximately 25
        posts = posts['data']

    else:
        posts = collect_endpoint( fbid , 'feed' )

    for post in posts:

        try:

            data[ post['id'] ] =  graph.get_object( post['id'] ,
                fields ='id,from,created_time,application,description,message,to,updated_time'
            ) ## to be compleated

            data[ post['id'] ][ 'comments' ] = collect_endpoint( post['id'], 'comments' )
            data[ post['id'] ][ 'likes' ] = collect_endpoint( post['id'], 'likes' )

        except facebook.GraphAPIError as e:
            def f():
                data[ post['id'] ] = { 'id' : post['id']  }
            handle_fb_errors( e, f )

    return data.values()

def collect_endpoint( fbid, endpoint ):
    ret = []

    try:
        d = graph.get_all_connections( id = fbid , connection_name=endpoint )
        for _d in d:
            ret.append( _d )

        return ret

    except facebook.GraphAPIError as e:
        handle_fb_errors( e , lambda:  collect_endpoint( fbid, endpoint ) )


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
        ## data['meta']['input_file'] = f
        data['meta']['collection_time'] = str( datetime.datetime.now() ) ## when data was collected

        return data

    except facebook.GraphAPIError as e:
        handle_fb_errors( e , lambda: collect_basics( fbid ) )

if __name__ == '__main__':

    import sys
    import datetime

    ii = len( sys.argv[1:] )

    for i, filename in enumerate( sys.argv[1:] ):

        jj = len( open(filename) )

        for j, url in enumerate( open(filename) ):

            print "File", i, "of", ii, "entry", j, "of", jj

            url = url.strip()
            fbid = url.split('?')[0]
            fbid = fbid.split('.com/')[1]
            ## remove list of bad terms
            for s in ['groups/']:
                fbid = fbid.replace(s, '')
            fbid = fbid.replace('/', '')

            ## data collection starts here

            data = collect_basics( fbid )

            fbtype = data['meta']['type']
            if fbtype in ['page', 'group', 'event', 'user']:
                data['feed'] = collect_feed( fbid )

            if fbtype in ['page', 'event']:
                data['photos'] = collect_endpoint( fbid, 'photos' )

            if fbtype == 'group':
                data['members'] = collect_endpoint( fbid, 'members')

            ## TODO: add group and page metadata collection

            json.dump( data, open( 'data/data_' + data['name'].replace(' ', '_').replace('/', '_').lower() + '.json', 'w' ), sort_keys=True, indent=4 )
