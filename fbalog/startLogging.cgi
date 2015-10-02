#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# JAHugawa's ToDo corner:
# DOJO: check if the logging path works >.<
# DOJO: check shell=True vulnerabilities!

import cgi
import cgitb # detailed error reports in browser when errors occur
import json
import shlex
import subprocess
import urllib.request

from AppConfiguration import *
from DbConnection import *
from FBDataFetcher import *
import TextToHtml as T2H

# set error logging/displaying
cgitb.enable(display=0, logdir=LOG_PATH) 

# create header
header = "Content-Type: text/html"
print(header)
print()

loginSuccessful = True # change to False when something goes horribly wrong
error = ""

# handle errors / fetch access token
form = cgi.FieldStorage()
if "error_reason" and "error" and "error_description" in form: #user denied request
    loginSuccessful = False
    error = form["error_description"].value
elif "code" in form:
    code = form["code"].value
    # proceed by sending access token request
    response = None
    try:
        response = urllib.request.urlopen("https://graph.facebook.com/v2.4/oauth/access_token?client_id="+APP_ID+"&redirect_uri="+REDIRECT_URI+"&client_secret="+APP_SECRET+"&code="+code)
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
    print("""<html><body><h1>Login successful! The code is crunching...</h1></body></html>""")
else:
    print("""<html><body><h1>Login failed! Reason: """+T2H.convert(error)+"""</h1></body></html>""")

