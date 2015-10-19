#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# JAHugawa's ToDo corner:
# DOJO: check if the logging path works >.<
# DOJO: check shell=True vulnerabilities!
# DOJO: python 2 (because of server configs >.<) so does not work with python3

from cgi import escape
#from flup.server.fcgi import WSGIServer
import json
import os
import shlex
import subprocess
import sys
import urllib.request # for urlopen
import urllib.parse # for parse_qs
from wsgiref.simple_server import make_server

from AppConfiguration import *
from DbConnection import *
from FBDataFetcher import *
import TextToHtml as T2H

def toBytes(s):
    return bytes(s,"ascii")

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    
    loginSuccessful = True # change to False when something goes horribly wrong
    error = ""

    # handle errors / fetch access token
    getParams = urllib.parse.parse_qs(environ["QUERY_STRING"])
    if "error_reason" and "error" and "error_description" in getParams: #user denied request
        loginSuccessful = False
        error = getParams["error_description"].value
    elif "code" in getParams:
        code = getParams["code"].value
        # proceed by sending access token request
        response = None
        try:
            response = urllib.request.urlopen("https://graph.facebook.com/v2.4/oauth/access_token?client_id="+APP_ID+"&redirect_uri="+REDIRECT_URI+"&response_type=code&scope=user_likes,user_posts,user_status&client_secret="+APP_SECRET+"&code="+code)
        except:
            loginSuccessful = False
            error = "Unknown error when starting logging. Please try again."
        else:
            if response.getcode() not in [200]:
                loginSuccessful = False
                error = "fetching long-term token failed with code "+response.getcode()
            else:
                d = json.loads(response.read())
                if set(["access_token","token_type","expires_in"]).issubset(set(d.keys())):
                    accessToken = d["access_token"]
                    # push access token to database
                    fb = FBDataFetcher()
                    userId = fb.fetchUserId(accessToken)
                    db = DbConnection()
                    db.setAccessToken(userId,accessToken)
                    # start remote process to mine the data, then proceed to tell the user that logging has successfully started
                    p = subprocess.Popen(args="python3 mineFB.py "+shlex.quote(userId), shell=True)
                else:
                    loginSuccessful = False
                    error = "response was missing data (access_token, token_type or expires_in)"

    else:
        loginSuccessful = False
        error = "missing authentication info (code). Try again"

    # end this process by returning success message
    if loginSuccessful:
        yield toBytes("<html><body><h1>Login successful! The code is crunching...</h1></body></html>")
    else:
        yield toBytes("<html><body><h1>Login failed! Reason: "+T2H.convert(error)+"</h1></body></html>")

port = 9090
kuplassaServer = make_server('localhost', port, app)
print("Kuplassa Server running on port %d" % port)
kuplassaServer.serve_forever()
