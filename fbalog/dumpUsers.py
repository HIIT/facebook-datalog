import json
import sys
import time

from AppConfiguration import *
from DbConnection import *
from FBDataFetcher import *

if __name__ == "__main__":
    db = DbConnection()
    fb = FBDataFetcher()
    
    userIds = []
    if len(sys.argv) >= 2:
        userIds += sys.argv[1:]
    else:
        # if no user ids are supplied, fetch all users
        userIds += db.getAllUserIds()
    
    # dump user id-name pairs to json
    userNames = {}
    for uid in userIds:
        accessToken = db.getAccessToken(uid)
        userNames[uid] = fb.fetchUserName(uid, accessToken)
    namesJson = json.dumps(userNames)
    currentTime = time.strftime("%Y_%m_%d_%H%M%S", time.gmtime())
    with open("users_%s.json" % (currentTime,),"w") as f:
        f.write(namesJson)

