import facebook
import requests
import json

keys = json.load( open('keys.json') )
app_id = keys['app-id']
app_secret = keys['app-secret']

graph = facebook.GraphAPI(access_token= app_id + '|' + app_secret, version='2.7')

def collect_feed( graph, id ):

    ## collect posts
    ## TODO: pagination to be added
    data = {}

    posts = graph.get_connections( id = id , connection_name='feed' )
    posts = posts['data']

    for post in posts:

        data[ post['id'] ] =  graph.get_object( post['id'] ,
            fields ='id,from,created_time,application,description,message,to,updated_time'
        ) ## to be compleated

        data[ post['id'] ][ '__comments' ] = graph.get_connections( id = post['id'], connection_name='comments' )['data']
        data[ post['id'] ][ '_likes' ] = graph.get_connections( id = post['id'], connection_name='likes' )['data']

    return data.values()

for line in open('wave0.txt'):

    try:

        line = line.strip()
        line = line.split('?')[0]
        line = line.split('.com/')[1]
        line = line.replace('/', '')

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

        ## TODO: add group and page metadata collection

        json.dump( data, open( 'data_' + fbobject['name'].replace(' ', '_').lower() + '.json', 'w' ) )


    except facebook.GraphAPIError:
        print line, 'failed'
