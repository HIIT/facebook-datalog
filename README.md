Various Facebook data logging utilities

code tested with python 3.4 without external libraries.



fbpetj: python script that takes your facebook access token and a list of facebook ids of public events. Then the script fetches data (basic information, feed, comments, likes, participation) of the event and pushes it to a json file.



fbalog: logs user's activity on facebook and pushes it to a sqlite3 database. Slow to execute (fb has rate limits).

To run fbalog, you need to create a file AppConfiguration.py. Put the following there:
LOGPATH = "path/where/you/want/errors/to/be/logged"
APPSECRET = "app secret you get from facebook"
APPID = "app id you get from facebook"
REDIRECT_URI = "https://url.to/start_logging.cgi&response_type=code&scope=user_likes,user_posts,user_status,read_stream,user_friends"



In case of questions ask Jesper (Jahu@slack).
