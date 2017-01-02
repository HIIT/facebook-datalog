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

log = open('error.log', 'w')

def handle_fb_errors( e , redo ):

    log.write( str(e) + '\n' )

    if e.code in [4, 17, 341]: ## application limit errors
        time.sleep( 60 * 60 ) ## one hour
        print "Sleeping: API says no"
        redo()
    else:
        print "Error", e


def collect_feed( fbid ):

    ## collect posts
    data = {}

    fields = """id,from,created_time,application,description,message,to,updated_time,
    likes{},
    comments{id,from,created_time,message,updated_time,likes{},comments{id,from,created_time,message,updated_time,likes{}}}"""
    ## check this is everything required


    fields.replace('\n', '' )

    if __DEV__:

        posts = graph.get_connections( id = fbid , connection_name='feed', fields = fields ) ## approximately 25
        posts = posts['data']

    else:
        posts = collect_endpoint( fbid , 'feed', fields = fields )

    return posts ## todo: postprocess

def collect_endpoint( fbid, endpoint, fields = None ):
    ret = []

    try:
        d = graph.get_all_connections( id = fbid , connection_name=endpoint, fields = fields )
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
        ## if we end up here, there wasn't anything esle to execute -> return False
        return False

if __name__ == '__main__':

    import sys
    import datetime

    collect_counter = 0

    ii = len( sys.argv[1:] )

    for i, filename in enumerate( sys.argv[1:] ):

        jj = len( open(filename).readlines() )

        for j, url in enumerate( open(filename) ):

            print "File", (i+1), "of", ii, "entry", (j+1), "of", jj

            url = url.strip()
            fbid = url.split('?')[0]
            fbid = fbid.split('.com/')[1]
            ## remove list of bad terms
            for s in ['groups/']:
                fbid = fbid.replace(s, '')
            fbid = fbid.replace('/', '')

            ## data collection starts here

            data = collect_basics( fbid )

            if data:

                fbtype = data['meta']['type']
                if fbtype in ['page', 'group', 'event', 'user']:
                    data['feed'] = collect_feed( fbid )

                if fbtype in ['page', 'event']:
                    data['photos'] = collect_endpoint( fbid, 'photos' )

                if fbtype == 'group':
                    data['members'] = collect_endpoint( fbid, 'members')

                ## TODO: add group and page metadata collection

                json.dump( data, open( 'data/data_' + data['name'].replace(' ', '_').replace('/', '_').lower() + '.json', 'w' ), sort_keys=True, indent=4 )

                collect_counter += 1

                if collect_counter % 20 == 0:
                    print "Sleeping: Time to relax"
                    time.sleep( 60 * 60 ) ## relax loading speed
