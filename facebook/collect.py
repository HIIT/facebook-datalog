# -*- coding: utf8

import sys
sys.path.insert( 0, '../../facebook-sdk/' ) ## temporary hack to use newer version of SDK

import facebook
import requests
import json
import time
import datetime

keys = json.load( open('keys.json') )
app_id = keys['app-id']
app_secret = keys['app-secret']

__DEV__ = False ## True ## Flag to test if we're running a development thing => limit the amount of data collected from feeds

graph = facebook.GraphAPI(access_token= app_id + '|' + app_secret, version="2.12")

now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
log = open('error_' + now + '.log', 'a')

def handle_fb_errors( fbid, e , redo ):

    log.write( fbid + ': ' + e.message.encode('utf8') + '\n' )

    if 'code' in e and e.code in [4, 17, 341]: ## application limit errors
        time.sleep( 60 * 60 ) ## one hour
        print "Sleeping: API says no"
        redo()
    else:
        print "Site:", fbid
        print "\t", e.message.encode('utf8')

## XXX: TODO: fix this mess
___scale = '10'
__commentfields = [
    'id',
    'from',
    'application',
    'created_time',
    'message',
    'updated_time',
    'permalink_url',
    'attachment',
    'object',
    'likes.limit(' + ___scale + '){}',
    'comments.limit(' + ___scale + '){id,from,created_time,message,updated_time,likes.limit(' + ___scale + '){}}'
]
__commentfields = ','.join( __commentfields )

__postfields = [
    'id',
    'from',
    'created_time',
    'message',
    'updated_time',
    'permalink_url,type',
    'caption',
    'description',
    'story',
    'link',
    'message_tags',
    'picture',
    'status_type',
    'to',
    'likes.limit(' + ___scale + ')',
    'comments.limit(' + ___scale + '){' + __commentfields + '}',
    'reactions.limit(' + ___scale + ')',
    'attachments',
    'sharedposts.limit(' + ___scale + ')'
]

__postfields = ','.join( __postfields )

print __postfields

def __collect_part_of_feed( post, field ):

    print post, field

    if field not in post: ## no comments on this post, just add the field
        post[ field ] = []

    elif 'paging' in post[ field ] and 'next' in post[ field ]['paging']: ## there is more data to collect!

        if field == 'comments':
            post[ field ] = collect_endpoint( post['id'], field, __commentfields )
        else:
            post[ field ] = collect_endpoint( post['id'], field )

    elif 'data' in post[field]:
        post[ field ] = post[ field ]['data'] ## remove pagination information

def collect_feed( fbid, since = '' ):

    ## collect posts
    data = {}

    ## XXX: check this is everything required

    if __DEV__:

        posts = graph.get_connections( id = fbid , connection_name='feed', fields = __postfields ) ## approximately 25
        posts = posts['data']

    else:
        posts = collect_endpoint( fbid , 'feed', fields = __postfields, since = since )


        print len( posts )

    ## check which posts have so many comments that we need to continue loading data from those
    ## also checks that data has fields defined and sets them as empty list if there is no such field
    for post in posts:

        post['comments'] = [] ## initialize as an empty array

        __collect_part_of_feed( post, 'comments' )
        __collect_part_of_feed( post, 'likes' )
        __collect_part_of_feed( post, 'reactions' )
        __collect_part_of_feed( post, 'sharedposts' )

        for comment in post['comments']:
            __collect_part_of_feed( comment, 'comments' )
            __collect_part_of_feed( comment, 'likes' )

    return posts

def collect_endpoint( fbid, endpoint, fields = None, since = '' ):
    ret = []

    try:
        d = graph.get_all_connections( id = fbid , connection_name=endpoint, fields = fields, since = since )
        for _d in d:
            ret.append( _d )

        return ret

    except facebook.GraphAPIError as e:
        handle_fb_errors( fbid, e , lambda:  collect_endpoint( fbid, endpoint ) )

    return ret

def collect_basics( fbid ):

    fbobject = graph.get_object(id = fbid, fields = 'id,name', metadata = '1')
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

def collect( fbid, previous_data = None ):

    data = graph.get_object(id = fbid, fields = 'id')
    fbid = data['id']

    if data:

        data = collect_basics( fbid )

        fbtype = data['meta']['type']

        if fbtype in ['page', 'group', 'event', 'user']:
            prev = []
            since = ''
            if previous_data:
               prev = previous_data['feed']
               since = max( map( lambda x: x['created_time'][:-5] , prev ) )
               print 'since', since
            data['feed'] = prev + collect_feed( fbid, since )

        if fbtype in ['page', 'event']:
            prev = []
            since = ''
            if previous_data:
               prev = previous_data['photos']
               since = max( map( lambda x: x['created_time'][:-5] , prev ) )
               print 'since', since
            data['photos'] = prev + collect_endpoint( fbid, 'photos', since )

        if fbtype == 'group':
            ## always rewire
            data['members'] = collect_endpoint( fbid, 'members')

    return data


if __name__ == '__main__':

    print facebook.__version__

    collect( '1363895887007159' )
