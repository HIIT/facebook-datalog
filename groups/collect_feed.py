import facebook
import requests
import json

keys = json.load( open('keys.json') )
app_id = keys['app-id']
app_secret = keys['app-secret']

graph = facebook.GraphAPI(access_token= app_id + '|' + app_secret, version='2.7')

for line in open('wave0.txt'):

    try:

        line = line.strip()
        line = line.split('?')[0]
        line = line.split('.com/')[1]
        line = line.replace('/', '')

        group = graph.get_object(id= line)

        ## collect posts
        ## TODO: pagination to be added

        data = {}

        posts = graph.get_connections( id = group['id'], connection_name='feed' )
        posts = posts['data']

        for post in posts:

            data[ post['id'] ] =  graph.get_object( post['id'] ,
                fields ='id,from,created_time,application,description,message,to,updated_time'
            ) ## to be compleated

            data[ post['id'] ][ '__comments' ] = graph.get_connections( id = post['id'], connection_name='comments' )['data']
            data[ post['id'] ][ '_likes' ] = graph.get_connections( id = post['id'], connection_name='likes' )['data']

        json.dump( data, open( 'data_' + line + '.json', 'w' ) )

    except facebook.GraphAPIError:
        print line, 'failed'
